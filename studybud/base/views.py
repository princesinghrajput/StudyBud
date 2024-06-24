from django.shortcuts import render


# Create your views here.

from django.http import HttpResponse

rooms = [
    {'id':1, 'name':'Lets learn Python'},
    {'id':2, 'name':'Lets learn Django'},
    {'id':3, 'name':'Lets learn Flask'},
    
]

def home(request):
    context = {'rooms':rooms}
    return render(request, 'base/home.html', context)

def room(request, pk):
    room =None
    for r in rooms:
        if r['id'] == int(pk):
            room = r
            
        context = {'room':room}
    return render(request, 'base/room.html', context)

