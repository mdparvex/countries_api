from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from .serializers import UserSignupSerializer
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view
from django.contrib.auth.models import User
from django.http import JsonResponse

class SignupView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = UserSignupSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token, _ = Token.objects.get_or_create(user=user)
            return Response({"token": token.key}, status=status.HTTP_201_CREATED)
        return Response({"detail":"Enter a valid username. This value may contain only letters, numbers, and @/./+/-/_ characters."}, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(username=username, password=password)
        if user:
            token, _ = Token.objects.get_or_create(user=user)
            return Response({"token": token.key})
        return Response({"detail": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
    
#create super user
@api_view(['GET'])
def create_superuser(request):
    User.objects.create_superuser('admin', 'admin@example.com', '12345678')

    return JsonResponse({'massege': 'ok'}, status=status.HTTP_200_OK)
