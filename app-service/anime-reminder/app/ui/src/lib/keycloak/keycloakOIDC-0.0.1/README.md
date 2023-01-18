# keycloakOIDC library

## Introduction

**keycloakOIDC** is a library to provide keycloak authorization mechanism to general  web frontend and backend service.

## Requirements

* Python 3.8 (Older and newer versions and not tested)

* Python3 package (would install automatically after run `python3 setup.py install`)

  ```python
  Flask >= 2.0.1
  httplib2 >= 0.20.2
  python-keycloak == 0.26.1
  jwt >= 1.3.1
  requests-oauthlib >= 1.3.0
  PyJWT >= 2.3.0
  ```

  

## Install

Open command line and go to the directory of **keycloakOIDC** and type:

```bash
python3 setup.py install
```



## Usage

### Backend

#### General

1. Inherit `KeycloakOIDCBackend` class, the template is shown below.

2. Implement all abstract class

   >If you only want to use `require_login` function, just need to implement `retrieve_header` and `raise_error` function.

   ```python
   from .keycloakOIDC_backend import KeycloakOIDCBackend
   
   
   class KeycloakOIDCBackendTest(KeycloakOIDCBackend):
   
     def __init__(self, *args, **kwargs):
       super().__init__(*args, **kwargs)
   
     @property
     def company_id(self) -> str:
       """Get the company_id from request url path"""
       return ""
       
     @property
     def project_id(self) -> str:
       """Get the project_id from request url path"""
       return ""
   
     def retrive_header(self) -> dict:
       return """Get header from request"""
   
     def raise_error(self, payload):
       return """Send response payload"""
   
   ```

3. Creat an instance with `client_secret_filename`, and use it as decorator to protect api. 

   ```python
   import KeycloakOIDCBackendTest
   
   client_secret_filename = "aiportal_secrets.json"
   koidc = KeycloakOIDCBackendTest(client_secret_filename)
   
   ### require_permission would header token and user role ###
   @koidc.require_permission("Default Resource")
   def api1():
     return 'success'
   
   ### require_login would check header token ###
   @koidc.require_login
   def api2():
     return 'success'
   ```

   **aiportal_secrets.json** (if environment not in pod)

   ```json
   {
       "client_name": "aiportal",
       "client_secret": "vzDr3w9R0wPpgXvwU2Mb0LLpAqaDAYCi",
       "host": "https://core.rpm.ai-platform/auth/",
       "realm_name": "aiplatform",
       "issuer": "https://core.rpm.ai-platform/auth/realms/aiplatform",
       "auth_uri": "https://core.rpm.ai-platform/auth/realms/aiplatform/protocol/openid-connect/auth",
       "userinfo_uri": "https://core.rpm.ai-platform/auth/realms/aiplatform/protocol/openid-connect/userinfo",
       "token_uri": "https://core.rpm.ai-platform/auth/realms/aiplatform/protocol/openid-connect/token",
       "token_introspection_uri": "https://core.rpm.ai-platform/auth/realms/aiplatform/protocol/openid-connect/token/introspect",
       "end_session_endpoint": "https://core.rpm.ai-platform/auth/realms/aiplatform/protocol/openid-connect/logout",
       "jwks_uri": "https://core.rpm.ai-platform/auth/realms/aiplatform/protocol/openid-connect/certs",
       "admin_username": "admin",
       "admin_password": "admin",
       "secret_key": "@!por+@l"
   }
   ```

   **aiportal_secrets.json** (if environment in pod)

   ```json
   {
       "client_name": "aiportal",
       "client_secret": "vzDr3w9R0wPpgXvwU2Mb0LLpAqaDAYCi",
       "host": "https://keycloak.ai-platform.svc.cluster.local/auth/",
       "realm_name": "aiplatform",
       "issuer": "https://keycloak.ai-platform.svc.cluster.local/auth/realms/aiplatform",
       "auth_uri": "https://keycloak.ai-platform.svc.cluster.local/auth/realms/aiplatform/protocol/openid-connect/auth",
       "userinfo_uri": "https://keycloak.ai-platform.svc.cluster.local/auth/realms/aiplatform/protocol/openid-connect/userinfo",
       "token_uri": "https://keycloak.ai-platform.svc.cluster.local/auth/realms/aiplatform/protocol/openid-connect/token",
       "token_introspection_uri": "https://keycloak.ai-platform.svc.cluster.local/auth/realms/aiplatform/protocol/openid-connect/token/introspect",
       "end_session_endpoint": "https://keycloak.ai-platform.svc.cluster.local/auth/realms/aiplatform/protocol/openid-connect/logout",
       "jwks_uri": "https://keycloak.ai-platform.svc.cluster.local/auth/realms/aiplatform/protocol/openid-connect/certs",
       "admin_username": "admin",
       "admin_password": "admin",
       "secret_key": "@!por+@l"
   }
   ```

​		



#### Flask

1. The `KeycloakOIDCBackendFlask` is already implemented, as below shown.

   ```python
   from flask import request, make_response, jsonify
   from .keycloakOIDC_backend import KeycloakOIDCBackend
   
   
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
       return jsonify(payload), int(payload["code"])
   ```
   
2. So just import and used it directly

   ```python
   from flask import Flask
   from keycloakOIDC import KeycloakOIDCBackendFlask
   
   koidc = KeycloakOIDCBackendFlask("aiportal.json")
   
   app = Flask(__name__)
   
   ### require_login would check header token ###
   @app.route("/api/v1/test1")
   @koidc.require_login
   def api2():
     return 'success'
   
   ### require_permission would check header token and check user permission ###
   @app.route("/api/v1/test2")
   @koidc.require_permission("Default Resource")
   def api1():
     return 'success'
   ```

   

### Frontend

#### Flask

1.  Import `KeycloakOIDCFrontendFlask` 

2. Create a `airportal.json` file and specify it when create an `KeycloakOIDCFrontendFlask` instance

   **aiportal_secrets.json** (if environment not in pod)

   ```json
   {
       "client_name": "aiportal",
       "client_secret": "vzDr3w9R0wPpgXvwU2Mb0LLpAqaDAYCi",
       "host": "https://core.rpm.ai-platform/auth/",
       "realm_name": "aiplatform",
       "issuer": "https://core.rpm.ai-platform/auth/realms/aiplatform",
       "auth_uri": "https://core.rpm.ai-platform/auth/realms/aiplatform/protocol/openid-connect/auth",
       "userinfo_uri": "https://core.rpm.ai-platform/auth/realms/aiplatform/protocol/openid-connect/userinfo",
       "token_uri": "https://core.rpm.ai-platform/auth/realms/aiplatform/protocol/openid-connect/token",
       "token_introspection_uri": "https://core.rpm.ai-platform/auth/realms/aiplatform/protocol/openid-connect/token/introspect",
       "end_session_endpoint": "https://core.rpm.ai-platform/auth/realms/aiplatform/protocol/openid-connect/logout",
       "jwks_uri": "https://core.rpm.ai-platform/auth/realms/aiplatform/protocol/openid-connect/certs",
       "admin_username": "admin",
       "admin_password": "admin",
       "secret_key": "@!por+@l"
   }
   ```

   **aiportal_secrets.json** (if environment in pod)

   ```json
   {
       "client_name": "aiportal",
       "client_secret": "vzDr3w9R0wPpgXvwU2Mb0LLpAqaDAYCi",
       "host": "https://keycloak.ai-platform.svc.cluster.local/auth/",
       "realm_name": "aiplatform",
       "issuer": "https://keycloak.ai-platform.svc.cluster.local/auth/realms/aiplatform",
       "auth_uri": "https://keycloak.ai-platform.svc.cluster.local/auth/realms/aiplatform/protocol/openid-connect/auth",
       "userinfo_uri": "https://keycloak.ai-platform.svc.cluster.local/auth/realms/aiplatform/protocol/openid-connect/userinfo",
       "token_uri": "https://keycloak.ai-platform.svc.cluster.local/auth/realms/aiplatform/protocol/openid-connect/token",
       "token_introspection_uri": "https://keycloak.ai-platform.svc.cluster.local/auth/realms/aiplatform/protocol/openid-connect/token/introspect",
       "end_session_endpoint": "https://keycloak.ai-platform.svc.cluster.local/auth/realms/aiplatform/protocol/openid-connect/logout",
       "jwks_uri": "https://keycloak.ai-platform.svc.cluster.local/auth/realms/aiplatform/protocol/openid-connect/certs",
       "admin_username": "admin",
       "admin_password": "admin",
       "secret_key": "@!por+@l"
   }
   ```

3. Use `require_login` or `require_permission`  to protect your view api

   ```python
   from flask import Flask, render_template
   from keycloakOIDC import KeycloakOIDCFrontendFlask
   
   app = Flask(__name__)
   koidc = KeycloakOIDCFrontendFlask(app, "aiportal.json")
   
   ### require_login would redirect to keycloak login page if not login yet ###
   @app.route('/view/v1/test1')
   @koidc.require_login
   def test1():
     
       return render_template('test1.html')
     
   ### require_permission would do require_login and also check user permission ###
   @app.route('/view/v1/test2')
   @koidc.require_permission("Default Resource")
   def test2():
     
       return render_template('test2.html')
    
   
   ```

   
