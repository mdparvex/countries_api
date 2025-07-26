from django.urls import path
from .views import SignupView, LoginView, create_superuser

urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('create-super-user/', create_superuser),
]
