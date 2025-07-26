import graphene
from .queries import Query
from .mutations.create import CreateCountry
from .mutations.update import UpdateCountry
from .mutations.delete import DeleteCountry

class Query(Query, graphene.ObjectType):
    pass

class Mutation(graphene.ObjectType):
    create_country = CreateCountry.Field()
    update_country = UpdateCountry.Field()
    delete_country = DeleteCountry.Field()

schema = graphene.Schema(query=Query,mutation=Mutation)
