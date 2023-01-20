
from flask import Blueprint, jsonify, request
from sqlalchemy import select, func, and_
from keycloakOIDC import KeycloakOIDCBackendFlask
from lib.db.db_manager import DBManager
from models.api.user import User
from models.api.anime import Anime
from models.db.user import User_DB, User_Anime_DB
from models.db.anime import Anime_DB
from lib.api.exceptions import OtherBadRequest, OtherNotFound
from lib.api.responses import Create, Update, Read, Delete

user_controller = Blueprint('user_controller', __name__)
koidc = KeycloakOIDCBackendFlask()

@user_controller.route('/animereminder/api/v1/user', methods=['GET'])
@koidc.require_login
# @koidc.require_permission("Default Resource")
def get_user():

    users = []
    with DBManager().session_ctx() as session:
        users_db = session.query(User_DB).all()
        for user_db in users_db:
            user = User(
                user_id=user_db.user_id
            )
            users.append(user)

    resp = Read(payload = users)
    return jsonify(resp.payload), resp.status_code

@user_controller.route('/animereminder/api/v1/user', methods=['POST'])
@koidc.require_login
# @koidc.require_permission("Default Resource")
def create_user():
    
    request_data = request.get_json()
    try:
        user = User(**request_data)
    except TypeError as e:
        raise OtherBadRequest('Invalid request data: %s'%e)

    user = _create_user()

    resp = Create(payload = user)
    return jsonify(resp.payload), resp.status_code

@user_controller.route('/animereminder/api/v1/user/<user_id>/anime', methods=['GET'])
@koidc.require_login
# @koidc.require_permission("Default Resource")
def get_user_anime(user_id):

    
    if not _is_user_exist(user_id):
        _create_user(user_id)

    users = []
    # with DBManager().session_ctx() as session:
    #     users_db = session.query(User_Anime_DB).filter_by(user_id = user_id).all()
    #     for user_db in users_db:
    #         print(user_db.user_id)
    with DBManager().session_ctx() as session:
        statement = (
            select(Anime_DB.anime_id, Anime_DB.anime_name)
            .join_from(User_Anime_DB, Anime_DB)
            .where(User_Anime_DB.user_id == user_id)
        )
        animes_db = session.execute(statement).all()
        animes = []
        for anime_db in animes_db:
            anime = Anime(
                anime_id=anime_db.anime_id,
                anime_name=anime_db.anime_name
            )
            animes.append(anime)

    resp = Read(payload = animes)
    return jsonify(resp.payload), resp.status_code

@user_controller.route('/animereminder/api/v1/user/<user_id>/anime', methods=['POST'])
@koidc.require_login
# @koidc.require_permission("Default Resource")
def create_user_anime(user_id):

    request_data = request.get_json()
    try:
        anime = Anime(**request_data)
    except TypeError as e:
        raise OtherBadRequest('Invalid request data: %s'%e)

    if not _is_user_exist(user_id):
        _create_user(user_id)

    with DBManager().session_ctx() as session:
        animes_db = session.query(Anime_DB).all()
        for anime_db in animes_db:
            # find the anime in anime list
            if anime.anime_name.lower().replace(" ","") == anime_db.anime_name.lower().replace(" ",""):
                anime.anime_id = anime_db.anime_id,
                anime.anime_name = anime_db.anime_name
        
        if anime.anime_id:
            ua_db = User_Anime_DB(
                user_id = user_id,
                anime_id = anime.anime_id
            )
            session.add(ua_db)
        else:
            raise OtherNotFound('No such anime found')

    resp = Create()
    return jsonify(resp.payload), resp.status_code

def _create_user(user_id):
    user_db = User_DB(
        user_id = user_id
    )
    with DBManager().session_ctx() as session:
        session.add(user_db)

    return User(user_id = user_id)

def _is_user_exist(user_id):
    with DBManager().session_ctx() as session:
        users_db = session.query(User_DB).all()
        for user_db in users_db:
            if str(user_id) == str(user_db.user_id):
                return True

    return False