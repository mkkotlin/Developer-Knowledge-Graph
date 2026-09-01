import strawberry
from strawberry.types import Info

from app.graphql.auth import require_user
from app.graphql.inputs.project import CreateProjectInput
from app.graphql.types.developer import ProjectType
from app.models.project import Project
from app.models.user import User
from app.graphql.utils import maybe_await


@strawberry.type
class ProjectMutation:

    @strawberry.mutation
    async def create_project(
        self,
        info: Info,
        input: CreateProjectInput,
    ) -> ProjectType:

        input.validate()

        user_id = require_user(info)

        db = info.context.db

        owner = await maybe_await(db.get(User, user_id))

        if owner is None:
            raise ValueError("Developer not found")

        project = Project(
            owner_id=user_id,
            name=input.name.strip(),
            description=input.description,
            status=input.status.value,
        )


        db.add(project)

        await maybe_await(db.commit())
        await maybe_await(db.refresh(project))

        return ProjectType(
            id=project.id,
            name=project.name,
            description=project.description,
            status=project.status,
        )



