import graphene
from countries_info_api.models.countries import Country

class DeleteCountry(graphene.Mutation):
    class Arguments:
        country_id = graphene.ID(required=True)

    ok = graphene.Boolean()
    message = graphene.String()

    def mutate(self, info, country_id):
        try:
            country = Country.objects.get(country_id=country_id)
            country.delete()
            return DeleteCountry(ok=True, message="Country deleted successfully.")
        except Country.DoesNotExist:
            return DeleteCountry(ok=False, message="Country not found.")
