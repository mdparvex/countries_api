import graphene
from graphene_django.types import DjangoObjectType
from countries_info_api.models.countries import Country
from countries_info_api.models.regions import Region
from countries_info_api.models.currencies import Currency
from countries_info_api.models.subregions import SubRegion
from countries_info_api.models.languages import Language
from countries_info_api.models.timezones import Timezone
from countries_info_api.models.continents import Continent
from countries_info_api.models.borders import Border
from countries_info_api.models.capitals import Capital

from ..queries import CountryType
from graphene.types.generic import GenericScalar

class CreateCountry(graphene.Mutation):
    class Arguments:
        name = GenericScalar(required=True)
        cca2 = graphene.String(required=True)
        region_id = graphene.ID(required=True)
        sub_region_id = graphene.ID()
        currency_ids = graphene.List(graphene.ID)
        language_ids = graphene.List(graphene.ID)
        timezone_ids = graphene.List(graphene.ID)
        continent_ids = graphene.List(graphene.ID)
        capital_ids = graphene.List(graphene.ID)

    country = graphene.Field(CountryType)

    def mutate(self, info, name, cca2, region_id, sub_region_id=None,
               currency_ids=[], language_ids=[], timezone_ids=[],
               continent_ids=[], capital_ids=[]):
        
        # We can do get_or create if object is missing database
        region = Region.objects.get(region_id=region_id)
        sub_region = SubRegion.objects.get(subregion_id=sub_region_id) if sub_region_id else None

        country = Country.objects.create(
            name=name,
            cca2=cca2,
            region=region,
            sub_region=sub_region
        )

        if currency_ids:
            country.currencies.set(Currency.objects.filter(currency_id__in=currency_ids))

        if language_ids:
            country.language.set(Language.objects.filter(language_id__in=language_ids))

        if timezone_ids:
            country.timezones.set(Timezone.objects.filter(timezone_id__in=timezone_ids))

        if continent_ids:
            country.continents.set(Continent.objects.filter(continent_id__in=continent_ids))

        if capital_ids:
            country.capitals.set(Capital.objects.filter(capital_id__in=capital_ids))

        country.save()
        return CreateCountry(country=country)


