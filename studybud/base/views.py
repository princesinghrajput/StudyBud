from django.shortcuts import render, redirect
from .models import Room, Topic
from .forms import RoomForm


# Create your views here.

from django.http import HttpResponse

# rooms = [
#     {'id':1, 'name':'Lets learn Python'},
#     {'id':2, 'name':'Lets learn Django'},
#     {'id':3, 'name':'Lets learn Flask'},
    
# ]

def home(request):
    q=request.GET.get('q') if request.GET.get('q') !=None else ''
    rooms = Room.objects.filter(topic__name__icontains=q)

    topics = Topic.objects.all()
    

    context = {'rooms':rooms, 'topics':topics}
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



def updateRoom(request, pk):
    room = Room.objects.get(id =pk)
    form = RoomForm(instance=room)

    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {'form': form}
    return render(request, 'base/room_form.html', context)


def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)
    if request.method == 'POST':
        room.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj':room})
