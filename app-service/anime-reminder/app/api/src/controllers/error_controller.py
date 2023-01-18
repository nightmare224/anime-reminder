from flask import jsonify, Blueprint
from lib.api.exceptions import (
    UserNotFound,
    OtherConflict,
    OtherBadRequest,
    OtherNotFound,
    Unauthenticated,
    PermissionDenied,
)

error_controller = Blueprint("error_controller", __name__)


@error_controller.app_errorhandler(UserNotFound)
def user_not_found_error(e):
    return jsonify(e.payload), e.status_code


@error_controller.app_errorhandler(OtherConflict)
def other_conflict_error(e):
    return jsonify(e.payload), e.status_code


@error_controller.app_errorhandler(OtherBadRequest)
def other_conflict_error(e):
    return jsonify(e.payload), e.status_code


@error_controller.app_errorhandler(OtherNotFound)
def other_not_found_error(e):
    return jsonify(e.payload), e.status_code


@error_controller.app_errorhandler(Unauthenticated)
def unauthenticated_error(e):
    return jsonify(e.payload), e.status_code


@error_controller.app_errorhandler(PermissionDenied)
def permission_denied_error(e):
    return jsonify(e.payload), e.status_code
