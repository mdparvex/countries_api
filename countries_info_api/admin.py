from django.contrib import admin
from .models.borders import Border
from .models.capitals import Capital
from .models.continents import Continent
from .models.countries import Country
from .models.currencies import Currency
from .models.demonyms import Demonym
from .models.gini import Gini
from .models.idd_suffixes import IddSuffix
from .models.idd import Idd
from .models.languages import Language
from .models.regions import Region
from .models.subregions import SubRegion
from .models.tld import Tld
from .models.translations import Translation
from .models.timezones import Timezone

# Register your models here.
admin.site.register(Border)
admin.site.register(Capital)
admin.site.register(Continent)
admin.site.register(Country)
admin.site.register(Currency)
admin.site.register(Demonym)
admin.site.register(Gini)
admin.site.register(IddSuffix)
admin.site.register(Idd)
admin.site.register(Language)
admin.site.register(Region)
admin.site.register(SubRegion)
admin.site.register(Tld)
admin.site.register(Translation)
admin.site.register(Timezone)
