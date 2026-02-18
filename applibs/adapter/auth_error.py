AUTHENTICATION_ERROR_CODES = {
    # Password strength
    "INVALID_PASSWORD": 5020,
    "PASSWORD_TOO_WEAK": 5021,
    # Change password
    "INCORRECT_OLD_PASSWORD": 5135,
    "MISSING_PASSWORD": 5138,
    "INVALID_NEW_PASSWORD": 5140,
}

class AuthenticationException(Exception):
    error_code = None
    error_message = None
    payload = {}

    def __init__(self, error_code, error_message, payload={}):
        self.error_code = error_code
        self.error_message = error_message
        self.payload = payload

    def get_error_dict(self):
        error = {"error_code": self.error_code, "error_message": self.error_message}
        for key in self.payload:
            error[key] = self.payload[key]

        return error