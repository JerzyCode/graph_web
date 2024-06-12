from app.utils.constants import MAX_VERTICES_PER_GRAPH, MAX_GRAPHS_PER_USER


class EmailTakenException(Exception):
    def __init__(self):
        self.message = "Email is already taken."


class InvalidPasswordException(Exception):
    def __init__(self):
        self.message = "Password is invalid."


class PasswordsDoNotMatchException(Exception):
    def __init__(self):
        self.message = "Passwords do not match."


class UserGraphCountExceededException(Exception):

    def __init__(self):
        self.message = f"User exceed graph count. Max number of graphs per user is ${MAX_GRAPHS_PER_USER}"


class GraphVertexCountExceededException(Exception):

    def __init__(self):
        self.message = f"Graph exceed vertices count. Max number of vertices per graph is ${MAX_VERTICES_PER_GRAPH}"
