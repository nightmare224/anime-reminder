
from flask import Blueprint, render_template, jsonify, request
from keycloakOIDC import KeycloakOIDCFrontendFlask

user_controller = Blueprint('user_controller', __name__)
koidc = KeycloakOIDCFrontendFlask()

@user_controller.route('/animereminder/ui/user', methods=['GET'])
# @koidc.require_permission("Default Resource")
@koidc.require_login
def get_user():

    return render_template('home.html')

@user_controller.route('/animereminder/ui/anime', methods=['GET'])
# @koidc.require_permission("Default Resource")
@koidc.require_login
def anime():

    return render_template('anime.html')


# @user_controller.route('/animereminder/api/v1/users', methods=['GET'])
# # @koidc.require_permission("Default Resource")
# def user():
#     print(request.headers)
#     return jsonify([{"anime_name":"spy family"}, {"anime_name":"chainsaw man"}]), 200


# from flask import request
# @user_controller.route('/animereminder/api/v1/anime', methods=['POST'])
# # @koidc.require_permission("Default Resource")
# def create_anime():
#     import random
#     request_data = request.get_json()
#     print(request_data)
#     return jsonify({"anime_id": f"{random.randint(1, 100000)}", "anime_name": "Chainsaw Man"}), 200