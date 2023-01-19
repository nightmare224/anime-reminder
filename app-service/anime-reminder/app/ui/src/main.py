
# from lib.config_parser_base import Config as RPSConfig
from configparser import ConfigParser
# from urllib.parse import quote as urlquote
from flask import Flask

# from lib.db.db_manager import DBManager
# controller
from controllers.user_controller import user_controller

from keycloakOIDC import KeycloakOIDCFrontendFlask
# import to create db
# import models.db.user

##### Setting #####
config_parser = ConfigParser()
config_parser.read("conf/config.ini")

# init flask app
app = Flask(__name__, static_url_path="/animereminder/ui")
# register controller
app.register_blueprint(user_controller)
app.config['OIDC_CALLBACK_ROUTE'] = '/animereminder/ui/_oidc_callback'
koidc = KeycloakOIDCFrontendFlask(app, "./lib/keycloak/secrets/anime-reminder-secrets.json")

@app.context_processor
def global_var():
    return dict(
        # USER_NAME = koidc.verify_and_decode_token(koidc.access_token)["username"],
        # USER_EMAIL = koidc.verify_and_decode_token(koidc.access_token)["email"],
        ACCESS_TOKEN = koidc.access_token,
        USER_ID = koidc.verify_and_decode_token(koidc.access_token)["sub"]
    )

if __name__ == '__main__':
    app.run(
        host = config_parser["FLASK"]["Host"],
        port = config_parser["FLASK"]["Port"],
        debug = config_parser["FLASK"]["DebugMode"],
        # ssl_context='adhoc'
    )