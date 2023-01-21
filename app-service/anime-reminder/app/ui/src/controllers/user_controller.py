
from flask import Blueprint, render_template, jsonify, request, redirect
from keycloakOIDC import KeycloakOIDCFrontendFlask

user_controller = Blueprint('user_controller', __name__)
koidc = KeycloakOIDCFrontendFlask()


@user_controller.route('/animereminder/ui/base', methods=['GET'])
@koidc.require_login
def base():

    return render_template('user.html')

@user_controller.route('/animereminder/ui/home', methods=['GET'])
# @koidc.require_permission("Default Resource")
@koidc.require_login
def home():

    return render_template('home.html')

@user_controller.route('/animereminder/ui/anime', methods=['GET'])
# @koidc.require_permission("Default Resource")
@koidc.require_login
def anime():
    return render_template('anime.html')


@user_controller.route('/animereminder/ui/user', methods=['GET'])
# @koidc.require_permission("Default Resource")
@koidc.require_login
def user():
    return render_template('user.html')

@user_controller.route('/animereminder/ui/logout')
# @koidc.require_login
def logout():

    # koidc.logout()
    uid = koidc.get_uid_cookie()
    credentials = koidc.credentials_store[uid]
    refresh_token = credentials.token["refresh_token"]
    
    koidc.keycloak_openid.logout(refresh_token)
    # clean credential store
    uid = koidc.get_uid_cookie()
    koidc.credentials_store.pop(uid)

    return redirect("/animereminder/ui/home")