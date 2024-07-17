from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db.models import Q
from .models import Room, Topic
from .forms import RoomForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm  

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

def registerPage(request):
    form= UserCreationForm()

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username=user.username.lower()

            user.save()
            login(request, user)
            return redirect('home')

        


    return render(request, 'base/login_register.html', {'form': form})



def loginPage(request):

    page='login'

    if request.user.is_authenticated:
        return redirect('home')

    if request.method=='POST':
        username= request.POST.get('username')
        password = request.POST.get('password')

       

        try:
            user = User.objects.get(username=username, password=password)
        except:
            messages.error(request, "User Does Not Exists!")

        user = authenticate(request, username=username, password=password)
       

        if user is not None:
            login(request, user)
            return redirect('home')


    context = {'page': page}
    return render(request, 'base/login_register.html', context)


def logoutUser(request):
    logout(request)
    return redirect('home')



def home(request):
    #! Query to fetch Room data from database

    q= request.GET.get('q') if request.GET.get('q') != None else ''
    print(q)
    rooms= Room.objects.filter(
      Q( name__icontains=q ) | 
      Q( description__icontains=q ) |
      Q( topic__name__icontains=q ) |
      Q( host__username__icontains=q )  
    )

    topics= Topic.objects.all()

    return render(request, 'base/home.html', context={'rooms':rooms, 'topics':topics})
    

def room(request, pk):
    #! Fetch Room data from database using room id
    room = Room.objects.get(id=pk)


    # room = None
    # for r in rooms:
    #     if r['id'] == int(pk):
    #         room = r
            
    context = {'room':room}
    return render(request, 'base/room.html', context)

@login_required(login_url='login')
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


@login_required(login_url='login')
def updateRoom(request, pk):
    room=Room.objects.get(id=pk)
    form=RoomForm(instance=room)

    if request.user != room.host:
        return HttpResponse("You are not allowed here!")

    if request.method == 'POST':
        form=RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')


    context={'form':form}

    return render(request,'base/room_form.html', context)


@login_required(login_url='login')
def deleteRoom(request, pk):
    room=Room.objects.get(id=pk)

    if request.user!= room.host:
        return HttpResponse("You are not allowed here!")

    if request.method == 'POST':
        room.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj':room})
        



   
    


def about(request):
    return render(request, 'base/about.html')