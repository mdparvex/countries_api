from django.urls import path
from .views.get_all_data import CountryListDetailsAPIView

urlpatterns = [
 path('list-all-countries-details/', CountryListDetailsAPIView.as_view()),
]