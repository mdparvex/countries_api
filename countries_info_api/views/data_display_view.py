from django.shortcuts import render

def country_list_view(request):
    return render(request, 'country_list.html')