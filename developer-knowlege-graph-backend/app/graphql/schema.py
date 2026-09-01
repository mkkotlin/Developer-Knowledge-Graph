import strawberry
from app.graphql.types.developer import DeveloperQuery
from app.graphql.mutations import SkillMutation
from app.graphql.project_mutations import ProjectMutation
from app.graphql.technology_mutations import TechnologyMutation
from app.graphql.project_skill_mutations import ProjectSkillMutation


@strawberry.type
class Query(DeveloperQuery):
    pass
    
@strawberry.type
class Mutation(SkillMutation, ProjectMutation, TechnologyMutation, ProjectSkillMutation):
    pass


schema = strawberry.Schema(query=Query, mutation=Mutation)