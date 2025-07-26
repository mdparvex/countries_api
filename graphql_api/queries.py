import graphene
from countries_info_api.models.countries import Country
from .types import CountryType

class Query(graphene.ObjectType):
    all_countries = graphene.List(CountryType)
    country_by_code = graphene.Field(CountryType, cca2=graphene.String(required=True))

    def resolve_all_countries(root, info):
        return Country.objects.select_related(
            'region', 'sub_region'
        ).prefetch_related(
            'currencies', 'language', 'timezones', 'continents', 'borders'
        ).all()
    def resolve_country_by_code(root, info, cca2):
        return Country.objects.filter(cca2=cca2).first()

