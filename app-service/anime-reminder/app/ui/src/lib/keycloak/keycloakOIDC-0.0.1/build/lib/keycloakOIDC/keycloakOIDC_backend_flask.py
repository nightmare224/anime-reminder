import logging
from flask import request, make_response, jsonify, abort
from .keycloakOIDC_backend import KeycloakOIDCBackend

logger = logging.getLogger(__name__)

class KeycloakOIDCBackendFlask(KeycloakOIDCBackend):

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)

  @property
  def company_id(self) -> str:
    return request.view_args["company_id"] if "company_id" in request.view_args else None

  @property
  def project_id(self) -> str:
    return request.view_args["project_id"] if "project_id" in request.view_args else None

  def retrive_header(self) -> dict:
    return request.headers

  def raise_error(self, payload):
    return abort(make_response(jsonify(payload), int(payload["code"])))