import json
from os import environ as env
from urllib.parse import quote_plus, urlencode

from authlib.integrations.flask_client import OAuth
from dotenv import find_dotenv, load_dotenv
from flask import Flask, redirect, render_template, session, url_for
from utils.log_config import Logger

# Initialize logger for this module
logger = Logger(__name__).get_logger()

ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)

app = Flask(__name__)
app.secret_key = env.get("APP_SECRET_KEY")
oauth = OAuth(app)

try:
    oauth.register(
        "auth0",
        client_id=env.get("AUTH0_CLIENT_ID"),
        client_secret=env.get("AUTH0_CLIENT_SECRET"),
        client_kwargs={
            "scope": "openid profile email",
        },
        server_metadata_url=f'https://{env.get("AUTH0_DOMAIN")}/.well-known/openid-configuration',
    )
    logger.info("OAuth setup completed.")
except Exception as e:
    logger.error("Failed to set up OAuth: %s", str(e))


# Controllers API
@app.route("/")
def home():
    try:
        user_info = json.dumps(session.get("user"), indent=4)
        logger.debug("Displayed home page with user info.")
        return render_template(
            "home.html", session=session.get("user"), pretty=user_info
        )
    except Exception as e:
        logger.error("Error displaying home page: %s", str(e))
        return render_template("error.html"), 500


@app.route("/callback", methods=["GET", "POST"])
def callback():
    try:
        token = oauth.auth0.authorize_access_token()
        session["user"] = token
        logger.info("User logged in successfully.")
        return redirect("/")
    except Exception as e:
        logger.error("Login callback failed: %s", str(e))
        return render_template("error.html"), 500


@app.route("/login")
def login():
    try:
        redirect_url = url_for("callback", _external=True)
        response = oauth.auth0.authorize_redirect(redirect_uri=redirect_url)
        logger.debug("Redirecting to login.")
        return response
    except Exception as e:
        logger.error("Login failed: %s", str(e))
        return render_template("error.html"), 500


@app.route("/logout")
def logout():
    try:
        session.clear()
        logout_url = (
            "https://"
            + env.get("AUTH0_DOMAIN")
            + "/v2/logout?"
            + urlencode(
                {
                    "returnTo": url_for("home", _external=True),
                    "client_id": env.get("AUTH0_CLIENT_ID"),
                },
                quote_via=quote_plus,
            )
        )
        logger.info("User logged out.")
        return redirect(logout_url)
    except Exception as e:
        logger.error("Logout failed: %s", str(e))
        return render_template("error.html"), 500


if __name__ == "__main__":
    try:
        app_port = env.get("PORT", 5000)
        logger.info("Starting server on port %s", app_port)
        app.run(host="0.0.0.0", port=app_port)
    except Exception as e:
        logger.error("Failed to start server: %s", str(e))
