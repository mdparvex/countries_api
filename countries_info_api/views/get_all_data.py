from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.core.cache import cache
from rest_framework import status
from ..models.countries import Country, CountryDetailsSerializer
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle

CACHE_TTL = 60 * 10

class CountryListDetailsAPIView(APIView):
    permission_classes = [IsAuthenticated]
    throttle_classes = [AnonRateThrottle, UserRateThrottle] #global throtolling

    def throttle_failure_view(self, request):
        return Response(
            {"error": "You have exceeded your request limit. Please try again later."},
            status=status.HTTP_429_TOO_MANY_REQUESTS
        )

    def get(self, request):
        cache_key = "all_country_list_with details"
        data = cache.get(cache_key)
        if data:
            return Response(data)
        countries = Country.objects.all()
        serializer_data = CountryDetailsSerializer(countries, many=True).data
        cache.set(cache_key, serializer_data, CACHE_TTL)
        return Response(serializer_data)
