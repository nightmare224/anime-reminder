import logging
from functools import wraps
from abc import ABC, abstractmethod
from .keycloakOIDC import KeycloakOIDC

logger = logging.getLogger(__name__)

class KeycloakOIDCBackend(KeycloakOIDC, ABC):
  
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    
  @property
  def access_token(self):
    return self.get_token_from_header()

  @abstractmethod
  def retrive_header(self) -> dict:
    return NotImplemented
  
  def require_login(self, api_func):
    @wraps(api_func)
    def decorated(*args, **kwargs):
      if self.verify_and_decode_token(self.access_token):
        return api_func(*args, **kwargs)
      else:
        return self.raise_error(self.unauthenticated_error())
    return decorated

  def require_permission(self, resource_name):
    def wrapper(func):
      @self.require_login
      @wraps(func)
      def decorated(*args, **kwargs):
        if self.verify_permission_from_token(self.access_token, resource_name):
          return func(*args, **kwargs)
        else:
          return self.raise_error(self.unauthorized_error())
      return decorated
    return wrapper
  
  def get_token_from_header(self):
    header = self.retrive_header()
    if "Authorization" not in header:
      return self.raise_error(self.badrequest_error("Token not provided"))

    try:
      schema, token = header["Authorization"].split()
    except:
      return self.raise_error(self.badrequest_error("Should be Bearer token"))

    if schema.lower() != "bearer":
      raise self.raise_error(self.badrequest_error("Should be Bearer token"))

    return token