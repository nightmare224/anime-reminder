
from flask import Blueprint, jsonify, request
from lib.db.db_manager import DBManager
from models.db.user import User_DB


user_controller = Blueprint('user_controller', __name__)


@user_controller.route('/animereminder/api/v1/users', methods=['GET'])
# @koidc.require_permission("Default Resource")
def get_user():
    with DBManager().session_ctx() as session:
        users_db = session.query(User_DB).all()
        for user_db in users_db:
            print(user_db.user_id)
    
    return '200'