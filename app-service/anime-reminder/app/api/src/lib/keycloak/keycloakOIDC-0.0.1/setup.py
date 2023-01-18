from setuptools import setup
import sys
from os.path import join, dirname

sys.path.append(join(dirname(__file__), 'keycloakOIDC'))

setup(
      name = "keycloakOIDC",
      version = "0.0.1",
      packages = ["keycloakOIDC"],
      install_requires = [
            "Flask >= 2.0.1",
            "httplib2 >= 0.20.2",
            "python-keycloak == 0.26.1",
            "requests-oauthlib >= 1.3.0",
            "PyJWT == 2.3.0",
            "urllib3 == 1.26.8",
            "cryptography == 37.0.2"
      ]
)
