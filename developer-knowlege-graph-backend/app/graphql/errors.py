class GraphQLError(Exception):
    code = "INTERNAL_ERROR"

    def __init__(self, message: str):
        super().__init__(message)
        self.message = message


class AuthenticationError(GraphQLError):
    code = "UNAUTHENTICATED"


class AuthorizationError(GraphQLError):
    code = "FORBIDDEN"


class NotFoundError(GraphQLError):
    code = "NOT_FOUND"


class ValidationError(GraphQLError):
    code = "VALIDATION_ERROR"


class ConflictError(GraphQLError):
    code = "CONFLICT"

