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

class RegionType(DjangoObjectType):
    class Meta:
        model = Region

class SubRegionType(DjangoObjectType):
    class Meta:
        model = SubRegion

class CurrencyType(DjangoObjectType):
    class Meta:
        model = Currency

class LanguageType(DjangoObjectType):
    class Meta:
        model = Language

class TimezonesType(DjangoObjectType):
    class Meta:
        model = Timezone

class CapitalsType(DjangoObjectType):
    class Meta:
        model = Capital

class ContinentType(DjangoObjectType):
    class Meta:
        model = Continent

class CountryType(DjangoObjectType):
    class Meta:
        model = Country

    region = graphene.Field(RegionType)
    sub_region = graphene.Field(SubRegionType)
    currencies = graphene.List(CurrencyType)
    language = graphene.List(LanguageType)
    timezones = graphene.List(TimezonesType)
    capitals = graphene.List(CapitalsType)
    continents = graphene.List(ContinentType)
    
    def resolve_region(self, info):
        return self.region
    
    def resolve_sub_region(self,info):
        return self.sub_region

    def resolve_currencies(self, info):
        return self.currencies.all()
    
    def resolve_language(self, info):
        return self.language.all()
    
    def resolve_timezones(self, info):
        return self.timezones.all()
    
    def resolve_capitals(self, info):
        return self.capitals.all()
    def resolve_continents(self, info):
        return self.continents.all()