from enum import Enum

import strawberry


@strawberry.enum
class ProjectStatus(Enum):
    ACTIVE = "ACTIVE"
    COMPLETED = "COMPLETED"
    ARCHIVED = "ARCHIVED"
