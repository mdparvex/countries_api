# views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from ..models.countries import Country, CountryDetailsSerializer

class CountryListDetailsAPIView(APIView):
    def get(self, request):
        countries = Country.objects.all()
        serializer = CountryDetailsSerializer(countries, many=True)
        return Response(serializer.data)
