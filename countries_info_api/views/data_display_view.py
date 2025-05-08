from django.shortcuts import render

def country_list_view(request):
    return render(request, 'country_list.html')

def signup(request):
    return render(request, 'signup.html')

def login(request):
    return render(request, 'login.html')