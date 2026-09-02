import strawberry


@strawberry.input
class DeveloperFilter:
    skills: list[str] | None = None
    technologies: list[str] | None = None
    min_proficiency: int | None = None




@strawberry.input
class ProjectFilter:
    technology: str | None = None
    skill: str | None = None
