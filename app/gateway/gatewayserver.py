import os

import gridfs
import pika
from bson.objectid import ObjectId
from decorators import requires_auth
from flask import Flask, request, send_file, session
from flask_pymongo import PyMongo
from storage import util

server = Flask(__name__)

mongo_video_uri = f"mongodb+srv://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@db-contentstore.mongocluster.cosmos.azure.com/videos"
mongo_mp3_uri = f"mongodb+srv://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@db-contentstore.mongocluster.cosmos.azure.com/mp3s"

mongo_video = PyMongo(server, uri=mongo_video_uri)
mongo_mp3 = PyMongo(server, uri=mongo_mp3_uri)

fs_videos = gridfs.GridFS(mongo_video.db)
fs_mp3s = gridfs.GridFS(mongo_mp3.db)

connection = pika.BlockingConnection(pika.ConnectionParameters("rabbitmq"))
channel = connection.channel()


@server.route("/upload", methods=["POST"])
@requires_auth
def upload():
    user_profile = session.get("user").get("userinfo")

    if user_profile:
        if len(request.files) > 1 or len(request.files) < 1:
            return "exactly 1 file required", 400

        for _, f in request.files.items():
            err = util.upload(f, fs_videos, channel, user_profile)

            if err:
                return err

        return "success!", 200
    else:
        return "not authorized", 401


@server.route("/download", methods=["GET"])
@requires_auth
def download():
    user_profile = session.get("user").get("userinfo")

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


if __name__ == "__main__":
    server.run(host="0.0.0.0", port=8080)
