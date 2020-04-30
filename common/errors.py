class HttpError(Exception):
    def __init__(self, status, message, payload=None):
        self.status = status
        self.message = message
        self.payload = payload or {}


class Http404Error(HttpError):
    def __init__(self, message=None, payload=None):
        super().__init__(status=404, message=message or 'Resource not found', payload=payload)


class Http400Error(HttpError):
    def __init__(self, message=None, payload=None):
        super().__init__(status=400, message=message or 'Bad payload', payload=payload)


class Http401Error(HttpError):
    def __init__(self, message=None, payload=None):
        super().__init__(status=401, message=message or 'Unauthorized', payload=payload)


class Http403Error(HttpError):
    def __init__(self, message=None, payload=None):
        super().__init__(status=403, message=message or 'Forbidden', payload=payload)


class Http409Error(HttpError):
    def __init__(self, message=None, payload=None):
        super().__init__(status=409, message=message or 'Resource already exist', payload=payload)


class Http410Error(HttpError):
    def __init__(self, message=None, payload=None):
        super().__init__(status=410, message=message or 'Resource not available anymore', payload=payload)
