class HTTPException:
    def __init__(self, status, data):
        self.status = status
        self.data = data
