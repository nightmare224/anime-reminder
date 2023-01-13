
from flask import Blueprint, jsonify, request
from lib.db.db_manager import DBManager
from models.api.user import User
from models.db.user import User_DB
from lib.api.responses import Create, Update, Read, Delete

user_controller = Blueprint('user_controller', __name__)


@user_controller.route('/animereminder/api/v1/users', methods=['GET'])
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