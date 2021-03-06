from django.shortcuts import render
from django.http import HttpResponse


def page_view(request):
    return HttpResponse('<h1><center>fuck you Umed</center></h1>')

# Create your views here.
