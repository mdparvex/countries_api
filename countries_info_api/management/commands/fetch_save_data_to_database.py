import logging
import requests
from time import sleep
from django.core.management.base import BaseCommand
from django.db import transaction, IntegrityError
from requests.exceptions import RequestException
from countries_info_api.models.borders import Border
from countries_info_api.models.capitals import Capital
from countries_info_api.models.continents import Continent
from countries_info_api.models.countries import Country
from countries_info_api.models.demonyms import Demonym
from countries_info_api.models.currencies import Currency
from countries_info_api.models.gini import Gini
from countries_info_api.models.idd_suffixes import IddSuffix
from countries_info_api.models.idd import Idd
from countries_info_api.models.languages import Language
from countries_info_api.models.regions import Region
from countries_info_api.models.subregions import SubRegion
from countries_info_api.models.tld import Tld
from countries_info_api.models.translations import Translation
from countries_info_api.models.timezones import Timezone

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

API_URL = "https://restcountries.com/v3.1/all"
MAX_RETRIES = 2
RETRY_DELAY = 2  # seconds


class Command(BaseCommand):
    help = "Fetch country data from REST Countries API and populate database"

    def handle(self, *args, **options):
        logger.info("Starting fetch of countries data...")

        for attempt in range(MAX_RETRIES):
            try:
                response = requests.get(API_URL, timeout=15)
                response.raise_for_status()
                countries_data = response.json()
                break
            except RequestException as e:
                logger.warning(f"Attempt {attempt + 1} failed: {e}")
                sleep(RETRY_DELAY)
        else:
            logger.error("Failed to fetch data after retries.")
            return

        for country_data in countries_data:
            try:
                with transaction.atomic():
                    self.process_country(country_data)
            except Exception as e:
                logger.exception(f"Error processing country {country_data.get('cca2', 'unknown')}: {e}")

        logger.info("Country data fetch and insertion complete.")

    def get_or_create_related(self, model, defaults=None, **lookup):
        obj, _ = model.objects.get_or_create(defaults=defaults or {}, **lookup)
        return obj

    def process_country(self, data):
        cca2 = data.get('cca2')
        if not cca2:
            logger.warning("Skipping country without cca2")
            return

        # Foreign keys
        region = self.get_or_create_related(Region, name=data.get('region')) if data.get('region') else None
        subregion = self.get_or_create_related(SubRegion, name=data.get('subregion')) if data.get('subregion') else None

        # Create country
        country, created = Country.objects.get_or_create(
            cca2=cca2,
            defaults={
                'name': data.get('name', {}),
                'ccn3': data.get('ccn3'),
                'cca3':data.get('cca3'),
                'cioc': data.get('cioc'),
                'independent': data.get('independent', False),
                'status': data.get('status'),
                'un_member': data.get('unMember', False),
                'altSpellings': data.get('altSpellings', []),
                'region': region,
                'sub_region': subregion,
                'latlng': data.get('latlng'),
                'landlocked': data.get('landlocked', False),
                'area': data.get('area'),
                'flag': data.get('flag'),
                'maps': data.get('maps', {}),
                'population': data.get('population'),
                'fifa': data.get('fifa'),
                'car': data.get('car', {}),
                'flags': data.get('flags', {}),
                'coatOfArms': data.get('coatOfArms', {}),
                'startOfWeek': data.get('startOfWeek'),
                'capitalInfo': data.get('capitalInfo', {}),
                'postalCode': data.get('postalCode', {}),
            }
        )

        if not created:
            logger.info(f"Country {cca2} already exists, skipping.")
            return
        
        #many-to-mant time zone
        timezone_objs = []
        timezone_data = data.get('timezones',[])
        for zone in timezone_data:
            obj = self.get_or_create_related(Timezone, zone=zone) if data.get('timezones') else None
            timezone_objs.append(obj)

        country.timezones.set(timezone_objs)
        #many-to-many continent
        continent_objs = []
        continets_data = data.get('continents',[])
        for con in continets_data:
            obj = self.get_or_create_related(Continent, name=con) if data.get('continents') else None
            continent_objs.append(obj)

        country.continents.set(continent_objs)
        # Many-to-many: currencies
        currencies_objs = []
        for code, cur in (data.get('currencies') or {}).items():
            currency = self.get_or_create_related(Currency, code=code, defaults={
                'name': cur.get('name'),
                'symbol': cur.get('symbol')
            })
            currencies_objs.append(currency)
        country.currencies.set(currencies_objs)

        # Many-to-many: languages
        languages = []
        for code, name in (data.get('languages') or {}).items():
            lang = self.get_or_create_related(Language, code=code, name=name)
            languages.append(lang)
        country.language.set(languages)

        # many-to-many: borders
        border_codes = data.get('borders',[])
        border_objs = []
        for border_code in border_codes:
            border_obj = self.get_or_create_related(Border, border_with=border_code)
            border_objs.append(border_obj)
        country.borders.set(border_objs)

        # One-to-many: capitals
        capital_names = data.get('capital', [])
        Capital.objects.bulk_create([
            Capital(name=name, country=country) for name in capital_names
        ])

        # Demonyms
        demonyms_data = data.get('demonyms', {})
        for lang_code, values in demonyms_data.items():
            Demonym.objects.create(
                country=country,
                language_code=lang_code,
                male=values.get('m'),
                female=values.get('f')
            )

        # Gini
        for year, value in (data.get('gini',{})).items():
            Gini.objects.create(country=country, year=year, value=value)

        # IDD and suffixes
        idd_data = data.get('idd', {})
        if 'root' in idd_data:
            idd = Idd.objects.create(root=idd_data['root'], country=country)
            for suffix in idd_data.get('suffixes', []):
                IddSuffix.objects.create(suffix=suffix, idd=idd)

        # TLD
        Tld.objects.bulk_create([
            Tld(domain_name=tld, country=country)
            for tld in data.get('tld', [])
        ])

        # Translations
        translations = data.get('translations', {})
        Translation.objects.bulk_create([
            Translation(
                country=country,
                language_code=code,
                official=val.get('official'),
                common=val.get('common')
            )
            for code, val in translations.items()
        ])

        logger.info(f"Inserted country {cca2}")
