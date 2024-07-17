from django.shortcuts import render, redirect
from django.db.models import Q
from django.contrib.auth.decorators import login_required

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages



from .models import Room, Topic
from .forms import RoomForm


# Create your views here.

from django.http import HttpResponse

# rooms = [
#     {'id':1, 'name':'Lets learn Python'},
#     {'id':2, 'name':'Lets learn Django'},
#     {'id':3, 'name':'Lets learn Flask'},
    
# ]

def loginPage(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')
    
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'User Does Not Exist')

        user= authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('home')
        
        else:
            messages.error(request, 'Username OR password does not exist')


    context = {'page': page}
    return render(request, 'base/login_register.html', context)

def logoutUser(request):
    logout(request)
    return redirect('home')

def registerPage(request):

    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            #some customization
            user= form.save(commit=False)
            user.username= user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        
        else:
            messages.error(request, 'An error occured during registrations')
            
           

    return render(request, 'base/login_register.html', {'form': form})
 


def home(request):

    q=request.GET.get('q') if request.GET.get('q') !=None else ''
    rooms = Room.objects.filter(
        Q(topic__name__contains=q) | 
        Q(name__icontains=q) |
        Q(description__icontains=q)
        )

    topics = Topic.objects.all()
    
    room_count = rooms.count()
    

    context = {'rooms':rooms, 'topics':topics, 'room_count':room_count}
    return render(request, 'base/home.html', context)

def room(request, pk):
    room = Room.objects.get(id=pk)
    context = {'room':room}
    return render(request, 'base/room.html', context)



@login_required(login_url='login')
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


@login_required(login_url='login')
def updateRoom(request, pk):
    room = Room.objects.get(id =pk)
    form = RoomForm(instance=room)


    # Restricting anyone to update with id
    if request.user != room.host:
        return HttpResponse('Youre not allowed here')

    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {'form': form}
    return render(request, 'base/room_form.html', context)

@login_required(login_url='login')
def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)


     # Restricting anyone to delete with id
    if request.user != room.host:
        return HttpResponse('Youre not allowed here')

    if request.method == 'POST':
        room.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj':room})
