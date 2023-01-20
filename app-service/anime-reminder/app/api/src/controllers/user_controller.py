
from flask import Blueprint, jsonify, request
from sqlalchemy import select, func, and_
from keycloakOIDC import KeycloakOIDCBackendFlask
from lib.db.db_manager import DBManager
from models.api.user import User
from models.api.anime import Anime, Anime_Reminder, Anime_Record
from models.db.user import User_DB, User_Anime_DB, User_Anime_Reminder_DB
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

    animes = _get_user_anime(user_id)

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

@user_controller.route('/animereminder/api/v1/user/<user_id>/anime/<anime_id>', methods=['PUT'])
@koidc.require_login
# @koidc.require_permission("Default Resource")
def edit_user_anime(user_id, anime_id):

    request_data = request.get_json()
 
    try:
        anime = Anime_Reminder(**request_data)
    except TypeError as e:
        raise OtherBadRequest('Invalid request data: %s'%e)

    anime_old = _get_user_anime(user_id, anime_id)
    if not anime_old:
        raise OtherNotFound("The anime not found for the user")
    
    # resp = Read(anime_old[0].anime_reminder[0].season)
    # return jsonify(resp.payload), resp.status_code
    # The season to episode mapping before update
    season2episode = dict([(r.season, r.episode) for r in anime_old[0].anime_reminder])
 
    with DBManager().session_ctx() as session:
        # statement = (
        #     select(User_Anime_Reminder_DB.season, User_Anime_Reminder_DB.episode)
        #     .join_from(User_Anime_DB, User_Anime_Reminder_DB)
        #     .where(User_Anime_DB.user_id == user_id, User_Anime_DB.anime_id == anime_id)
        # )
        # reminders_db = session.execute(statement).all()
        index, = session.query(User_Anime_DB.index).filter_by(user_id = user_id, anime_id = anime_id).one()
        
        for reminder in anime.anime_reminder:
            # update the exist season
            if reminder.season in season2episode:
                session.query(User_Anime_Reminder_DB).filter_by(index = index, season = reminder.season).update(
                    dict(
                        episode = reminder.episode
                    )
                )
            # new the season
            else:
                session.add(
                    User_Anime_Reminder_DB(
                        index = index,
                        season = reminder.season,
                        episode = reminder.episode
                    )
                )

        # animes = []
        # for anime_db in animes_db:
        #     anime = Anime(
        #         anime_id=anime_db.anime_id,
        #         anime_name=anime_db.anime_name
        #     )
        #     animes.append(anime)



    resp = Update()
    return jsonify(resp.payload), resp.status_code

def _create_user(user_id):
    user_db = User_DB(
        user_id = user_id
    )
    with DBManager().session_ctx() as session:
        session.add(user_db)

    return User(user_id = user_id)

def _get_user_anime(user_id, anime_id = None):
    with DBManager().session_ctx() as session:
        statement = (
            select(Anime_DB.anime_id, Anime_DB.anime_name, User_Anime_DB.index)
            .join_from(User_Anime_DB, Anime_DB)
            .where(User_Anime_DB.user_id == user_id)
        )
        animes_db = session.execute(statement).all()
        animes = []
        for anime_db in animes_db:
            if (anime_id is None) or (str(anime_db.anime_id) == str(anime_id)):
                reminders_db = session.query(User_Anime_Reminder_DB).filter_by(index = anime_db.index).all()
                anime = Anime_Reminder(
                    anime_id=anime_db.anime_id,
                    anime_name=anime_db.anime_name,
                    anime_reminder = [Anime_Record(season = reminder_db.season, episode = reminder_db.episode) for reminder_db in reminders_db]
                )
                animes.append(anime)

    return animes

def _is_user_exist(user_id):
    with DBManager().session_ctx() as session:
        users_db = session.query(User_DB).all()
        for user_db in users_db:
            if str(user_id) == str(user_db.user_id):
                return True

    return False