class Create():
    def __init__(self, payload = None):
        self.status_code = 201
        if payload is None:
            self.payload = {
                "message": "created",
                "code": str(self.status_code),
                "status": "success"
            }
        else:
            self.payload = payload

class Read():
    def __init__(self, payload = None):
        self.status_code = 200
        if payload is None:
            self.payload = {
                "message": "ok",
                "code": str(self.status_code),
                "status": "success"
            }
        else:
            self.payload = payload

class Update():
    def __init__(self, payload = None):
        self.status_code = 200
        if payload is None:
            self.payload = {
                "message": "updated",
                "code": str(self.status_code),
                "status": "success"
            }
        else:
            self.payload = payload

class Delete():
    def __init__(self, payload = None):
        self.status_code = 200
        if payload is None:
            self.payload = {
                "message": "deleted",
                "code": str(self.status_code),
                "status": "success"
            }
        else:
            self.payload = payload