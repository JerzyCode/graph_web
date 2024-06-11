class EmailTakenException(Exception):
    def __init__(self):
        self.message = "Email is already taken."


class InvalidPasswordException(Exception):
    def __init__(self):
        self.message = "Password is invalid."


class PasswordsDoNotMatchException(Exception):
    def __init__(self):
        self.message = "Passwords do not match."
