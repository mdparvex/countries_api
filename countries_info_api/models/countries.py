from django.db import models
from rest_framework import serializers
from django.contrib.postgres.fields import ArrayField
from .regions import Region
from .subregions import SubRegion
from .languages import Language
from .currencies import Currency
from .continents import Continent
from .timezones import Timezone
from .borders import Border

class Country(models.Model):
    country_id = models.BigAutoField(primary_key=True)
    name = models.JSONField(default=dict)
    cca2 = models.CharField(max_length=10, unique=True)
    ccn3 = models.CharField(max_length=10, null=True, blank=True)
    cioc = models.CharField(max_length=10, null=True, blank=True)
    independent = models.BooleanField(default=False)
    status = models.CharField(max_length=100, null=True, blank=True)
    un_member = models.BooleanField(default=False)
    currencies = models.ManyToManyField(Currency, null=True, blank=True, related_name='countries')
    altSpellings = ArrayField(models.CharField(max_length=255), null=True, blank=True)
    region = models.ForeignKey(Region, null=True, on_delete=models.CASCADE, related_name='region_countries')
    sub_region = models.ForeignKey(SubRegion, null=True, on_delete=models.CASCADE, related_name='subregion_countries')
    language = models.ManyToManyField(Language, related_name='language_countries')
    latlng = ArrayField(models.CharField(max_length=255), null=True, blank=True)
    landlocked = models.BooleanField(default=False)
    area = models.FloatField(null=True)
    cca3 = models.CharField(max_length=10)
    flag = models.CharField(max_length=10, null=True, blank=True)
    maps = models.JSONField(default=dict)
    population = models.IntegerField(null=True)
    fifa = models.CharField(max_length=10, null=True, blank=True)
    car = models.JSONField(default=dict)
    timezones = models.ManyToManyField(Timezone, related_name='timezone_countries')
    continents = models.ManyToManyField(Continent, related_name='continent_countries')
    borders = models.ManyToManyField(Border, related_name='border_countries')
    flags = models.JSONField(default=dict)
    coatOfArms = models.JSONField(default=dict)
    startOfWeek = models.CharField(max_length=10, null=True, blank=True)
    capitalInfo = models.JSONField(default=dict)
    postalCode = models.JSONField(default=dict)

    def __str__(self):
        return self.name.get('common', self.cca2)
    
class CountryDetailsSerializer(serializers.ModelSerializer):
    borders = serializers.SerializerMethodField()
    capital = serializers.SerializerMethodField()
    currencies = serializers.SerializerMethodField()
    languages = serializers.SerializerMethodField()
    translations = serializers.SerializerMethodField()
    tld = serializers.SerializerMethodField()
    demonyms = serializers.SerializerMethodField()
    gini = serializers.SerializerMethodField()
    idd = serializers.SerializerMethodField()
    timezones = serializers.SerializerMethodField()
    continents = serializers.SerializerMethodField()

    class Meta:
        model = Country
        fields = [
            'name', 'tld', 'cca2', 'ccn3', 'cioc', 'independent',
            'status', 'un_member', 'currencies', 'idd', 'capital',
            'altSpellings', 'region', 'sub_region', 'languages','latlng', 'landlocked', 
            'borders', 'area', 'demonyms','cca3','translations', 'flag', 'maps',
            'population', 'gini', 'fifa', 'car', 'timezones', 'continents',
            'flags', 'coatOfArms', 'startOfWeek', 'capitalInfo', 'postalCode'
        ]

    def get_capital(self, obj):
        return [cap.name for cap in obj.capitals.all()]

    def get_borders(self, obj):
        return [b.border_with for b in obj.borders.all()]

    def get_currencies(self, obj):
        currencies = obj.currencies.all()
        return {
            c.code: {
                "name": c.name,
                "symbol": c.symbol
            } for c in currencies
        }

    def get_languages(self, obj):
        return {lang.code: lang.name for lang in obj.language.all()}

    def get_translations(self, obj):
        return {
            t.language_code: {
                "official": t.official,
                "common": t.common
            } for t in obj.translations.all()
        }

    def get_tld(self, obj):
        return [tld.domain_name for tld in obj.tlds.all()]

    def get_demonyms(self, obj):
        return {
            d.language_code: {
                "f": d.female,
                "m": d.male
            } for d in obj.demonyms.all()
        }

    def get_gini(self, obj):
        return {
            g.year: g.value for g in obj.gini_scores.all()
        }

    def get_idd(self, obj):
        if hasattr(obj, 'idd'):
            return {
                "root": obj.idd.root,
                "suffixes": [s.suffix for s in obj.idd.suffixes.all()]
            }
        return {}

    def get_timezones(self, obj):
        return [tz.zone for tz in obj.timezones.all()]

    def get_continents(self, obj):
        return [c.name for c in obj.continents.all()]
    
class CountrySerializer(serializers.ModelSerializer):
    capital = serializers.SerializerMethodField()
    timezones = serializers.SerializerMethodField()
    languages = serializers.SerializerMethodField()

    class Meta:
        model = Country
        fields = ['country_id','name', 'cca2', 'capital', 'population', 'timezones', 'flag', 'languages']

    def get_capital(self, obj):
        return [cap.name for cap in obj.capitals.all()]
    def get_timezones(self, obj):
        return [tz.zone for tz in obj.timezones.all()]
    def get_languages(self, obj):
        return {lang.code: lang.name for lang in obj.language.all()}
    
class CountryCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = '__all__'
    
