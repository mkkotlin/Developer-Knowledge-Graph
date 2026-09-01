import strawberry

from app.graphql.enums import ProjectStatus


@strawberry.input
class CreateProjectInput:
    name: str
    description: str | None = None
    status: ProjectStatus = ProjectStatus.ACTIVE

    def validate(self) -> None:
        if not self.name.strip():
            raise ValueError(
                "Project name cannot be empty"
            )

