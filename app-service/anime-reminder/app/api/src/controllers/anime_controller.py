
from flask import Blueprint, jsonify, request
from keycloakOIDC import KeycloakOIDCBackendFlask
from lib.db.db_manager import DBManager
from models.api.user import User
from models.api.anime import Anime
from models.db.user import User_DB
from models.db.anime import Anime_DB
from lib.api.responses import Create, Update, Read, Delete
from lib.api.exceptions import OtherBadRequest
from uuid import uuid1

anime_controller = Blueprint('anime_controller', __name__)
koidc = KeycloakOIDCBackendFlask()

@anime_controller.route('/animereminder/api/v1/anime', methods=['GET'])
@koidc.require_login
def get_anime():

    animes = []
    with DBManager().session_ctx() as session:
        animes_db = session.query(Anime_DB).all()
        for anime_db in animes_db:
            anime = Anime(
                anime_id=anime_db.anime_id,
                anime_name=anime_db.anime_name
            )
            animes.append(anime)

    resp = Read(payload = animes)
    return jsonify(resp.payload), resp.status_code

@anime_controller.route('/animereminder/api/v1/anime', methods=['POST'])
@koidc.require_login
# @koidc.require_permission("Default Resource")
def create_anime():
    
    request_data = request.get_json()
    try:
        animes = []
        for anime in request_data:
            anime = Anime(**anime)
            animes.append(anime)
    except TypeError as e:
        raise OtherBadRequest('Invalid request data: %s'%e)

    with DBManager().session_ctx() as session:
        
        for anime in animes:
            anime.anime_id = str(uuid1())
            # anime.anime_name
            anime_db = Anime_DB(
                anime_id = anime.anime_id,
                anime_name = anime.anime_name
            )
            session.add(anime_db)


    resp = Create(payload = animes)
    return jsonify(resp.payload), resp.status_code


# @anime_controller.route('/animereminder/api/v1/anime/<anime_id>', methods=['PUT'])
# # @koidc.require_permission("Default Resource")
# def edit_anime():

#     users = []
#     with DBManager().session_ctx() as session:
#         users_db = session.query(User_DB).all()
#         for user_db in users_db:
#             user = User(
#                 user_id=user_db.user_id
#             )
#             users.append(user)

#     resp = Read(payload = users)
#     return jsonify(resp.payload), resp.status_code