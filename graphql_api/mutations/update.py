import graphene
from graphene.types.generic import GenericScalar
from countries_info_api.models.countries import Country
from ..types import CountryType

class UpdateCountry(graphene.Mutation):
    class Arguments:
        country_id = graphene.ID(required=True)
        name = GenericScalar(required=False)
        region_id = graphene.Int(required=False)
        sub_region_id = graphene.Int(required=False)

    country = graphene.Field(CountryType)

    def mutate(self, info, country_id, **kwargs):
        try:
            country = Country.objects.get(country_id=country_id)
        except Country.DoesNotExist:
            raise Exception("Country not found")

        for attr, value in kwargs.items():
            print(f'attribute: {attr}, value: {value}')
            #We can add get_or create here if any objects missinng in database
            setattr(country, attr, value)

        country.save()
        return UpdateCountry(country=country)
