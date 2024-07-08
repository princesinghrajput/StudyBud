from django.shortcuts import render, redirect
from .models import Room
from .forms import RoomForm


# Create your views here.

from django.http import HttpResponse

# rooms = [
#     {'id':1, 'name':'Lets learn Python'},
#     {'id':2, 'name':'Lets learn Django'},
#     {'id':3, 'name':'Lets learn Flask'},
    
# ]

def home(request):
    rooms = Room.objects.all()
    

    context = {'rooms':rooms}
    return render(request, 'base/home.html', context)

def room(request, pk):
    room = Room.objects.get(id=pk)
    context = {'room':room}
    return render(request, 'base/room.html', context)



def create_room(request):
    form = RoomForm()
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
        print(request.POST)
    context={'form': form}
    return render(request, 'base/room_form.html', context)