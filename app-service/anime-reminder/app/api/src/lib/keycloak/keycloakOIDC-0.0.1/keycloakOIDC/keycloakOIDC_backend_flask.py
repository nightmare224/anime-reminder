import logging
from flask import request, make_response, jsonify, abort
from .keycloakOIDC_backend import KeycloakOIDCBackend

logger = logging.getLogger(__name__)

class KeycloakOIDCBackendFlask(KeycloakOIDCBackend):

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)

  def retrive_header(self) -> dict:
    return request.headers

  def raise_error(self, payload):
    return abort(make_response(jsonify(payload), int(payload["code"])))