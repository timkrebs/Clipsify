import json
import os
from urllib.parse import quote_plus, urlencode

import gridfs
import pika
import pymongo
from authlib.integrations.flask_client import OAuth
from bson.objectid import ObjectId
from decorators import requires_auth
from dotenv import find_dotenv, load_dotenv
from flask import Flask, redirect, render_template, request, send_file, session, url_for

ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)

server = Flask(__name__)
#server.secret_key = env.get("APP_SECRET_KEY")
#CONNECTION_STRING = env.get("MONGO_CONNECTION_STRING")
server.secret_key = os.getenv("APP_SECRET_KEY")
CONNECTION_STRING = os.getenv("MONGO_CONNECTION_STRING")


client = pymongo.MongoClient(CONNECTION_STRING)
try:
    client.server_info()  # validate connection string
except pymongo.errors.ServerSelectionTimeoutError:
    raise TimeoutError(
        "Invalid API for MongoDB connection string or timed out when \
            attempting to connect"
    )
video_db = client["videos"]
mp3_db = client["mp3"]
fs_videos = gridfs.GridFS(video_db)
fs_mp3s = gridfs.GridFS(mp3_db)

connection = pika.BlockingConnection(pika.ConnectionParameters("rabbitmq"))
channel = connection.channel()


@server.route("/upload", methods=["POST"])
@requires_auth
def upload():
    user_profile = session.get("user")

    if user_profile:
        if "file" not in request.files or request.files["file"].filename == "":
            return "exactly 1 file required", 400
        file = request.files["file"]

        try:
            fid = fs_videos.put(file, filename=file.filename)
            print(f"File uploaded successfully, file ID: {fid}")

        except Exception as e:
            print(f"Error uploading file: {e}")
            return "internal server error - upload not successful", 500

        message = {
            "video_fid": str(fid),
            "mp3_fid": None,
            "username": user_profile["userinfo"]["email"],
        }
        print(f"Message: {message}")

        try:
            channel.basic_publish(
                exchange="",
                routing_key="video",
                body=json.dumps(message),
                properties=pika.BasicProperties(delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE),
            )
        except Exception as err:
            print(err)
            fs_videos.delete(fid)
            return f"internal server error {err}", 500

        return "success!", 200
    else:
        return "not authorized", 401


@server.route("/download", methods=["GET"])
@requires_auth
def download():
    user_profile = session.get("user")

    if user_profile:
        fid_string = request.args.get("fid")

        if not fid_string:
            return "fid is required", 400

        try:
            out = fs_mp3s.get(ObjectId(fid_string))
            return send_file(out, download_name=f"{fid_string}.mp3")
        except Exception as err:
            print(err)
            return "internal server error", 500

    return "not authorized", 401


oauth = OAuth(server)

oauth.register(
    "auth0",
    #client_id=env.get("AUTH0_CLIENT_ID"),
    #client_secret=env.get("AUTH0_CLIENT_SECRET")
    client_id = os.getenv("AUTH0_CLIENT_ID"),
    client_secret=os.getenv("AUTH0_CLIENT_SECRET"),
    client_kwargs={
        "scope": "openid profile email",
    },
    server_metadata_url=f'https://{os.getenv("AUTH0_DOMAIN")}/.well-known/openid-configuration',
)


# Controllers API
@server.route("/")
def home():
    return render_template(
        "home.html",
        session=session.get("user"),
        pretty=json.dumps(session.get("user"), indent=4),
    )


@server.route("/callback", methods=["GET", "POST"])
def callback():
    token = oauth.auth0.authorize_access_token()
    session["user"] = token
    return redirect("/")


@server.route("/login")
def login():
    return oauth.auth0.authorize_redirect(redirect_uri=url_for("callback", _external=True))


@server.route("/logout")
def logout():
    session.clear()
    return redirect(
        "https://"
        + os.getenv("AUTH0_DOMAIN")#env.get("AUTH0_DOMAIN")
        + "/v2/logout?"
        + urlencode(
            {
                "returnTo": url_for("home", _external=True),
                "client_id": os.getenv("AUTH0_CLIENT_ID") #env.get("AUTH0_CLIENT_ID"),
            },
            quote_via=quote_plus,
        )
    )


if __name__ == "__main__":
    server.run(host="0.0.0.0", port=8080)