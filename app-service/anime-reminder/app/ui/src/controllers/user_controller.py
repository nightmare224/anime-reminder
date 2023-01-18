
from flask import Blueprint, render_template, jsonify, request
from keycloakOIDC import KeycloakOIDCFrontendFlask

user_controller = Blueprint('user_controller', __name__)
koidc = KeycloakOIDCFrontendFlask()

@user_controller.route('/animereminder/ui/v1/users', methods=['GET'])
# @koidc.require_permission("Default Resource")
@koidc.require_login
def get_user():

    return render_template('home.html')

@user_controller.route('/animereminder/api/v1/users', methods=['GET'])
# @koidc.require_permission("Default Resource")
def user():
    print(request.headers)
    return jsonify([{"anime_name":"spy family"}, {"anime_name":"chainsaw man"}]), 200