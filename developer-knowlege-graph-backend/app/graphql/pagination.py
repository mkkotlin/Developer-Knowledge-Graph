import base64
from typing import Annotated, TYPE_CHECKING
import strawberry

if TYPE_CHECKING:
    from app.graphql.types.developer import DeveloperType, ProjectType


def encode_cursor(value: int) -> str:
    return base64.b64encode(
        str(value).encode()
    ).decode()


def decode_cursor(cursor: str) -> int:
    return int(
        base64.b64decode(cursor.encode()).decode()
    )


@strawberry.type
class PageInfo:
    has_next_page: bool
    end_cursor: str | None


@strawberry.type
class ProjectEdge:
    node: Annotated["ProjectType", strawberry.lazy("app.graphql.types.developer")]
    cursor: str


@strawberry.type
class ProjectConnection:
    edges: list[ProjectEdge]
    page_info: PageInfo


@strawberry.type
class DeveloperEdge:
    node: Annotated["DeveloperType", strawberry.lazy("app.graphql.types.developer")]
    cursor: str


@strawberry.type
class DeveloperConnection:
    edges: list[DeveloperEdge]
    page_info: PageInfo

