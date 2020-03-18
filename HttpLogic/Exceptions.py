class RestrictedError(Exception):
    def __init__(self, message, api_message):
        super().__init__(message)
        self.api_message = api_message


class NotFoundError(Exception):
    def __init__(self, message, api_message):
        super().__init__(message)
        self.api_message = api_message


class NotValidError(Exception):
    def __init__(self, message, api_message):
        super().__init__(message)
        self.api_message = api_message


class NotEditableError(Exception):
    def __init__(self, message, api_message):
        super().__init__(message)
        self.api_message = api_message


class ReadOnlyTokenError(Exception):
    pass
