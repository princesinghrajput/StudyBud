from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

from django.http import HttpResponse

def home(request):
    return HttpResponse("Hello, world. You're at the polls index.")

def room(request):
    return HttpResponse("Hello, world.Room Index.")

