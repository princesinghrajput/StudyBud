from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Room
from .forms import RoomForm

# Create your views here.

# rooms = [
#     {'id':1, 'name':'Learn Javascript in 5 minutes'},
#     {'id':2, 'name':'Learn Python in 10 minutes'},
#     {'id':3, 'name':'Learn Java in 15 minutes'},
#     {'id':4, 'name':'Learn C++ in 20 minutes'},
#     {'id':5, 'name':'Learn C# in 25 minutes'},
#     {'id':6, 'name':'Learn Go in 30 minutes'},
#     {'id':7, 'name':'Learn Rust in 35 minutes'},
#     {'id':8, 'name':'Learn Rust in 35 minutes'},
# ]




def home(request):
    #! Query to fetch Room data from database

    rooms= Room.objects.all()

    return render(request, 'base/home.html', context={'rooms':rooms})
    

def room(request, pk):
    #! Fetch Room data from database using room id
    room = Room.objects.get(id=pk)


    # room = None
    # for r in rooms:
    #     if r['id'] == int(pk):
    #         room = r
            
    context = {'room':room}
    return render(request, 'base/room.html', context)


def createRoom(request):
    form=RoomForm()
    if request.method == 'POST':
        print(request.POST)
        form=RoomForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('home')



    context={'form':form}

    return render(request,'base/room_form.html', context)

def updateRoom(request, pk):
    room=Room.objects.get(id=pk)
    form=RoomForm(instance=room)

    if request.method == 'POST':
        form=RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')


    context={'form':form}

    return render(request,'base/room_form.html', context)



   
    


def about(request):
    return render(request, 'base/about.html')