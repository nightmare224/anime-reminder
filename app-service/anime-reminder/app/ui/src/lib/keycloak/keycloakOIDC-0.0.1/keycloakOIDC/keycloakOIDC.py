import jwt
import httplib2
import json
import re
import logging
import threading
from keycloak import KeycloakAdmin, KeycloakOpenID
from abc import ABC, abstractmethod

logger = logging.getLogger(__name__)

class KeycloakOIDC(ABC):

  _instance = None
  _lock = threading.Lock()

  def __new__(cls, *args, **kwargs):
    if not cls._instance:
      with cls._lock:
        if not cls._instance:
          cls._instance = super().__new__(cls)

    return cls._instance

  def __init__(self, client_secret_json = None):
    if self.initialized: return
    if not self.load_client_secrets(client_secret_json): return 
    self.keycloak_admin = KeycloakAdmin(
      server_url = self.client_secrets['host'], 
      username = self.client_secrets['admin_username'],
      password = self.client_secrets['admin_password'],
      realm_name = self.client_secrets['realm_name'], 
      client_id = 'admin-cli',
      auto_refresh_token = ['get', 'put', 'post', 'delete'],
      verify = True)
    self.keycloak_openid = KeycloakOpenID(
      server_url = self.client_secrets['host'],
      realm_name = self.client_secrets['realm_name'],
      client_id = self.client_secrets['client_name'],
      client_secret_key = self.client_secrets['client_secret'],
      verify = True)
    self.client_secrets["client_id"] = self.keycloak_admin.get_client_id(self.client_secrets['client_name'])
    self.roleSet = set(["Admin", "User"])
    self.initialized = True

  @property
  def initialized(self):
    try:
      return self._initialized
    except AttributeError: 
      return False
  @initialized.setter
  def initialized(self, initialized):
    self._initialized = initialized

  @property
  @abstractmethod
  def access_token(self):
    return NotImplemented

  
  @property
  def is_admin(self) -> bool:
    return "Admin" in self.retrive_user_roles_from_token(self.access_token)

  @property
  def is_user(self) -> bool:
    return "User" in self.retrive_user_roles_from_token(self.access_token)


  @abstractmethod
  def require_login(self):
    return NotImplemented

  @abstractmethod
  def require_permission(self):
    return NotImplemented

  @abstractmethod
  def raise_error(self, payload):
    return NotImplemented

  def badrequest_error(self, errmsg = ""):
    payload = {
      "message": errmsg or "Bad request",
      "code": "400",
      "status": "error"
    }
    return payload

  def unauthenticated_error(self, errmsg = ""):
    payload = {
      "message": errmsg or "Authentication requried",
      "code": "401",
      "status": "error"
    }
    return payload

  def unauthorized_error(self, errmsg = ""):
    payload = {
      "message": errmsg or "Permission denied",
      "code": "403",
      "status": "error"
    }
    return payload

  def notfound_error(self, errmsg = ""):
    payload = {
      "message": errmsg or "Not found",
      "code": "404",
      "status": "error"
    }
    return payload

  @property
  def public_key(self) -> str:
    publicKey = self.keycloak_openid.public_key()
    return f"-----BEGIN PUBLIC KEY-----\n{publicKey}\n-----END PUBLIC KEY-----".encode('ascii')

  def load_client_secrets(self, client_secret_json):
    try:
      with open(client_secret_json, "r") as f:
        self.client_secrets = json.loads(f.read())
    except:
      self.client_secrets = {}

    return self.client_secrets


  def verify_and_decode_token(self, token):
    try:
      token_decode = jwt.decode(token, self.public_key, algorithms=["RS256"], options = {'verify_exp': True, 'verify_aud': False})
      return token_decode
    except jwt.exceptions.ExpiredSignatureError:
      return self.raise_error(self.unauthenticated_error("Token expired"))
    except jwt.exceptions.InvalidSignatureError:
      return self.raise_error(self.unauthenticated_error("Signature verification failed"))
    except Exception as e:
      return self.raise_error(self.unauthenticated_error("Invalid token: %s" % e))

  def verify_permission_from_token(self, token, resource_name):
    uid = self.verify_and_decode_token(token)["sub"]
    roles = self.retrive_user_roles_from_token(token)
    # Get target resource
    resource_list = json.loads(self.keycloak_admin.get_client_authz_resources(self.client_secrets["client_id"]).content)
    target_resource = None
    for resource in resource_list:
      if resource["name"] == resource_name:
        target_resource = resource
        break
    # Resource not found
    if not target_resource: 
      return False
    # Evaluate
    access_token = self.keycloak_admin.token['access_token']
    http = httplib2.Http()
    resp, content = http.request(
      uri = f'{self.client_secrets["host"]}admin/realms/{self.client_secrets["realm_name"]}/clients/{self.client_secrets["client_id"]}/authz/resource-server/policy/evaluate',
      method = "POST",
      body = json.dumps(
        {
          "resources": [target_resource],
          "roleIds": list(roles),
          "userId": uid
        }
      ),
      headers={"Content-Type": "application/json", "Authorization": f"Bearer {access_token}"}
    )

    return json.loads(content)["status"] == "PERMIT"
    
  def retrive_user_roles_from_token(self, token):

    token_decode = self.verify_and_decode_token(token)
    roles = token_decode["resource_access"][self.client_secrets['client_name']]["roles"]
            
    return set(roles) & self.roleSet
