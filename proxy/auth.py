


class AuthenticationError(ValueError):
    def __init__(self, message="Authentication failed"):
        self.message = message
        super().__init__(self.message)
