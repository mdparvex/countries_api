from django.urls import path
from .views.get_all_data import CountryListDetailsAPIView
from .views.country_api_view import *

urlpatterns = [
 path('list-all-countries-details/', CountryListDetailsAPIView.as_view()), #this API return all data in actual format
 #API's for country related info
 path('all-countries/', get_all_country_list),
 path('country/', CountryAPIView.as_view()),
 path('same-region-country-list/<int:country_id>/', same_regional_country_list),
 path('same-language/countries/', countries_same_language),
 path('search-country/', search_country)
]