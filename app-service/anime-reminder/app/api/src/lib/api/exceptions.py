class UserNotFound(Exception):
    def __init__(self):
        super().__init__()
        self.status_code = 404
        self.payload = {
            "message": "User not found",
            "code": str(self.status_code),
            "status": "error"
        }


class OtherConflict(Exception):
    def __init__(self, msg = None):
        super().__init__()
        self.status_code = 409
        self.payload = {
            "message": msg or "Conflict",
            "code": str(self.status_code),
            "status": "error"
        }

class OtherBadRequest(Exception):
    def __init__(self, msg = None):
        super().__init__()
        self.status_code = 400
        self.payload = {
            "message": msg or "Bad request",
            "code": str(self.status_code),
            "status": "error"
        }

class OtherNotFound(Exception):
    def __init__(self, msg = None):
        super().__init__()
        self.status_code = 404
        self.payload = {
            "message": msg or "Not found",
            "code": str(self.status_code),
            "status": "error"
        }
        
class OtherBadRequest(Exception):
    def __init__(self, msg = None):
        super().__init__()
        self.status_code = 400
        self.payload = {
            "message": msg or "Bad request",
            "code": str(self.status_code),
            "status": "error"
        }

class Unauthenticated(Exception):
    def __init__(self, msg = None):
        super().__init__()
        self.status_code = 401
        self.payload = {
            "message": msg or "Authentication requried",
            "code": str(self.status_code),
            "status": "error"
        }

class PermissionDenied(Exception):
    def __init__(self, msg = None):
        super().__init__()
        self.status_code = 403
        self.payload = {
            "message": msg or "Permission denied",
            "code": str(self.status_code),
            "status": "error"
        }

