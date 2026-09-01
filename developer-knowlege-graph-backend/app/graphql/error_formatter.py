from typing import Any

from graphql import GraphQLError

from app.graphql.errors import GraphQLError as DomainError


def format_error(error: GraphQLError) -> dict[str, Any]:
    original = error.original_error

    if isinstance(original, DomainError):
        return {
            "message": original.message,
            "extensions": {
                "code": original.code,
            },
        }

    return {
        "message": "Internal server error",
        "extensions": {
            "code": "INTERNAL_ERROR",
        },
    }
