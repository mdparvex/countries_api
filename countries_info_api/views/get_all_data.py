from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.core.cache import cache
from ..models.countries import Country, CountryDetailsSerializer

CACHE_TTL = 60 * 10

class CountryListDetailsAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        cache_key = "all_country_list_with details"
        data = cache.get(cache_key)
        if data:
            return Response(data)
        countries = Country.objects.all()
        serializer_data = CountryDetailsSerializer(countries, many=True).data
        cache.set(cache_key, serializer_data, CACHE_TTL)
        return Response(serializer_data)
