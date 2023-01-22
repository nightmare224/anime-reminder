
# from lib.config_parser_base import Config as RPSConfig
from os import getenv
from configparser import ConfigParser
from urllib.parse import quote as urlquote
from flask import Flask

from keycloakOIDC import KeycloakOIDCBackendFlask
from lib.db.db_manager import DBManager
# controller
from controllers.user_controller import user_controller
from controllers.anime_controller import anime_controller
from controllers.error_controller import error_controller


##### Setting #####
config_parser = ConfigParser()
config_parser.read("conf/config.ini")
# connect to db
DBManager().db_uri(
    "default",
    "{}://{}:{}@{}:{}/{}".format(
        config_parser["DATABASE"]["Connector"],
        getenv("DB_USER"),
        urlquote(getenv("DB_PASSWORD")),
        config_parser["DATABASE"]["Host"],
        config_parser["DATABASE"]["Port"],
        config_parser["DATABASE"]["DatabaseName"],
    ),
    pool_size=5,
    pool_timeout=30,
)
# init flask app
app = Flask(__name__)
# register controller
app.register_blueprint(user_controller)
app.register_blueprint(anime_controller)
app.register_blueprint(error_controller)

# keycloak
koidc = KeycloakOIDCBackendFlask(f"./lib/keycloak/secrets/anime-reminder-secrets.json")

if __name__ == '__main__':
    app.run(
        host = config_parser["FLASK"]["Host"],
        port = config_parser["FLASK"]["Port"],
        debug = config_parser["FLASK"]["DebugMode"]
    )