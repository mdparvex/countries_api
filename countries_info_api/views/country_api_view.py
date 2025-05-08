from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from django.http import JsonResponse
from rest_framework import status
from django.core.cache import cache
from django.db.models.expressions import RawSQL
from ..models.countries import Country, CountrySerializer, CountryCreateUpdateSerializer
from ..models.regions import Region

CACHE_TTL = 60 * 10

class CountryAPIView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        content = {
            'status' :0
        }
        
        country_id = request.query_params.get("country_id")
        if not country_id:
            content['massege'] = 'country id require'
            return JsonResponse(content, status=status.HTTP_400_BAD_REQUEST)
        try:
            country = Country.objects.get(country_id=country_id)
        except Country.DoesNotExist:
            content['massege'] = 'country not found'
            return Response(content, status=status.HTTP_404_NOT_FOUND)
        
        serializer_data = CountrySerializer(country).data
        content['status'] = 1
        content['data'] = serializer_data
        return JsonResponse(content, status=status.HTTP_200_OK)
    
    def post(self, request):
        content = {
            'status' :0
        }
        serializer = CountryCreateUpdateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            content['status'] = 1
            content['massege'] = 'country created successfully'
            return JsonResponse(content, status=status.HTTP_201_CREATED)
        
        content['massege'] = 'validation failed to create'
        content['error'] = serializer.errors
        return JsonResponse(content, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        content = {
            'status' :0
        }
        country_id = request.data.get('country_id')
        if not country_id:
            content['massege'] = 'country id require'
            return JsonResponse(content, status=status.HTTP_400_BAD_REQUEST)
        try:
            country = Country.objects.get(country_id=country_id)
        except Country.DoesNotExist:
            content['massege'] = 'country not found'
            return Response(content, status=status.HTTP_404_NOT_FOUND)
        serializer = CountryCreateUpdateSerializer(country, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            content['status'] = 1
            content['massege'] = 'country created successfully'
            return JsonResponse(content, status=status.HTTP_200_OK)
        
        content['massege'] = 'validation failed to update'
        content['error'] = serializer.errors
        return JsonResponse(content, status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request, country_id):
        content = {
            'status' :0
        }
        
        try:
            country = Country.objects.get(country_id=country_id)
        except Country.DoesNotExist:
            content['massege'] = 'country not found'
            return Response(content, status=status.HTTP_404_NOT_FOUND)
        country.delete()
        content['status'] = 1
        content['massege'] = 'succesfully deleted'
        return Response(content, status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def get_all_country_list(request):
    content = {}
    cache_key = "all_country_list_"
    data = cache.get(cache_key)
    if data:
        content['status'] = 1
        content['data'] = data
        return JsonResponse(content, status=status.HTTP_200_OK)
    
    countries = Country.objects.all()
    serializer = CountrySerializer(countries, many=True)
    cache.set(cache_key, serializer.data, CACHE_TTL)

    content['status'] = 1
    content['data'] = serializer.data
    return JsonResponse(content, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def same_regional_country_list(request, country_id):
    content = {
        "status": 0
    }
    try:
        country = Country.objects.get(country_id=country_id)
    except Country.DoesNotExist:
        content['massege'] = 'country not found'
        return Response(content, status=status.HTTP_404_NOT_FOUND)
    
    country_objs = Country.objects.filter(region=country.region).exclude(country_id=country_id)
    country_data = CountrySerializer(country_objs, many=True).data
    content['status'] = 1
    content['data'] = country_data
    return JsonResponse(content, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def search_country(request):
    content = {
        "status": 0
    }
    query = request.query_params.get("name", "").strip().lower()
    print(query)
    if not query:
        content['massege'] = 'search name not found'
        return JsonResponse(content, status=status.HTTP_400_BAD_REQUEST)
    countries = Country.objects.annotate(
        common_name_lower=RawSQL("LOWER(name->>'common')", [])
    ).filter(common_name_lower__icontains=query)
    serializer = CountrySerializer(countries, many=True)

    content['status'] = 1
    content['data'] = serializer.data
    return JsonResponse(content, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def countries_same_language(request):
    content = {
        "status": 0
    }
    lang_code = request.query_params.get("lang_name")
    if not lang_code:
        content['massege'] = 'Query parameter not found'
        return JsonResponse(content, status=status.HTTP_400_BAD_REQUEST)

    countries = Country.objects.filter(language__name=lang_code).distinct()
    serializer = CountrySerializer(countries, many=True)

    content['status']=1
    content['data'] = serializer.data
    return JsonResponse(content, status=status.HTTP_200_OK)
