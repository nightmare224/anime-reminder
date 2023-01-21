import logging
import time
import jwt
import re
from flask import request, g, url_for, abort, redirect, session, make_response, jsonify, abort
from requests_oauthlib import OAuth2Session
from functools import wraps
from .keycloakOIDC import KeycloakOIDC

logger = logging.getLogger(__name__)

class KeycloakOIDCFrontendFlask(KeycloakOIDC):
  def __init__(self, app = None, *args, **kwargs):
    # if self.initialized: return
    super().__init__(*args, **kwargs)
    if app:
      self.init_app(app)
      self.credentials_store = {}

  @property
  def access_token(self):
    uid = self.get_uid_cookie()
    if uid not in self.credentials_store:
      #TODO: Clean KeycloakIdentity and KeycloakIdentityLegancy cookie to make sure it won't 502
      return None

    credentials = self.credentials_store[uid]
    if time.time() >= credentials.token["expires_at"]:
      try:
        token = credentials.refresh_token(
          token_url = self.client_secrets["token_uri"],
          client_id = self.client_secrets["client_name"],
          client_secret = self.client_secrets["client_secret"]
        )
      except:
        return None
      self.credentials_store[uid] = OAuth2Session(token = token)
      credentials = self.credentials_store[uid]

    return credentials.token["access_token"]

  @property
  def refresh_token(self):
    uid = self.get_uid_cookie()
    if uid not in self.credentials_store:
      return None
    credentials = self.credentials_store[uid]
    # # refresh token expires
    # if time.time() >= credentials.token["refresh_expires_at"]:
    #   return None
    
    return credentials.token["refresh_token"]

  def get_uid_cookie(self):
    try:
      uid_cookie_name = "uid"
      uid_cookie = request.cookies.get(uid_cookie_name)
      uid = jwt.decode(uid_cookie, self.client_secrets["secret_key"], algorithms = ["HS256"])["uid"]
      return uid
    except:
      return None

  def set_uid_cookie(self, response):
    uid_cookie_name = "uid"
    signed_uid = jwt.encode({"uid": g.uid}, self.client_secrets["secret_key"], algorithm = "HS256")
    response.set_cookie(
      uid_cookie_name,
      signed_uid,
      secure = True,
      httponly = True
    )

  def init_app(self, app):
    app.config['SECRET_KEY'] = '@n!me-rem!nder'
    app.route(app.config['OIDC_CALLBACK_ROUTE'])(self._oidc_callback)
    app.before_request(self._before_request)
    app.after_request(self._after_request)


  def _after_request(self, response):
    if g.uid:
      self.set_uid_cookie(response)

    return response

  def _before_request(self):
    g.uid = None
    # return self.authenticate_or_redirect()

  def _oidc_callback(self):
    oidc_session = self.generate_oidc_session(state = session["oauth_state"])
    
    token = oidc_session.fetch_token(
      self.client_secrets["token_uri"], 
      client_secret = self.client_secrets["client_secret"], 
      code = request.args['code'])
    token['refresh_expires_at'] = token['expires_at'] - token['expires_in'] + token['refresh_expires_in']
    g.uid = self.verify_and_decode_token(token["access_token"])["sub"]
    self.credentials_store[g.uid] = OAuth2Session(token = token)


    # TODO: Maybe Redirect to home page
    return redirect(session["destination"])

  def generate_oidc_session(self, **kwargs):

    return OAuth2Session(
      self.client_secrets["client_name"],
      scope = ["openid","email","profile","offline_access"],
      redirect_uri = url_for("_oidc_callback", _external = True),
      **kwargs)

  def redirect_to_auth_server(self, destination):
    oidc_session = self.generate_oidc_session()
    authorization_url, state = oidc_session.authorization_url(self.client_secrets["auth_uri"])
    session["oauth_state"] = state
    session["destination"] = destination
    
    return redirect(authorization_url)

  # TODO: maybe move to upper level
  def require_login(self, view_func):
    @wraps(view_func)
    def decorated(*args, **kwargs):
      try:
        self.verify_and_decode_token(self.access_token)
        return view_func(*args, **kwargs)
      except:
        return self.redirect_to_auth_server(request.url)
    return decorated  

  def require_permission(self, resource_name):
    def wrapper(func):
      @wraps(func)
      def decorated(*args, **kwargs):
        # need login first
        try:
          self.verify_and_decode_token(self.access_token)
        except:
          return self.redirect_to_auth_server(request.url)
        # check permission
        if self.verify_permission_from_token(self.access_token, resource_name):
          return func(*args, **kwargs)
        else:
          return self.raise_error(self.unauthorized_error())
      return decorated
    return wrapper

  def logout(self):
    # logout session
    refresh_token = self.refresh_token
    if refresh_token is not None:
      self.keycloak_openid.logout(refresh_token)
    # clean credential store
    uid = self.get_uid_cookie()
    if uid is not None:
      self.credentials_store.pop(uid)

  def retrive_current_user_roles(self):
    return self.retrive_user_roles_from_token(self.access_token)

  def raise_error(self, payload):
    return abort(int(payload["code"]), payload["message"])