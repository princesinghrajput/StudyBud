from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db.models import Q
from .models import Room, Topic, Message
from .forms import RoomForm, UserForm

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
            user = User.objects.get(username=username)
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

    topics= Topic.objects.all()[0:5]

    room_message = Message.objects.filter(Q(room__topic__name__icontains = q))

    room_counts= rooms.count()

    return render(request, 'base/home.html', context={'rooms':rooms, 'topics':topics, 'room_message': room_message, 'room_counts': room_counts})
    

def room(request, pk):
    #! Fetch Room data from database using room id
    room = Room.objects.get(id=pk)
    room_message= room.message_set.all().order_by('-created_at')
    participants= room.participants.all()

    if request.method == 'POST':
        message= Message.objects.create(
            user=request.user,
            room=room,
            body=request.POST.get('body')
        )
        room.participants.add(request.user)
        return redirect('room', pk=room.id)
 
            
    context = {'room':room, 'room_message':room_message, 'participants':participants}
    return render(request, 'base/room.html', context)

def userProfile(request, pk):
    user = User.objects.get(id=pk)
    room= user.room_set.all()
    topic = Topic.objects.all()
    room_message = user.message_set.all()
   
   

    context={'user': user, 'rooms': room, 'topics':topic, 'room_message': room_message}

    return render(request, 'base/profile.html', context)

@login_required(login_url='login')
def createRoom(request):
    topic = Topic.objects.all()
    form=RoomForm()
    if request.method == 'POST':
        print(request.POST)
        form=RoomForm(request.POST)

        if form.is_valid():
            room = form.save(commit=False)
            room.host = request.user
            form.save()
            return redirect('home')



    context={'form':form, 'topics':topic}

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



@login_required(login_url='login')
def deleteMessage(request, pk):
    message=Message.objects.get(id=pk)

    if request.user!= message.user:
        return HttpResponse("You are not allowed here!")

    if request.method == 'POST':
        message.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj':message})
        

@login_required(login_url='login')
def updateProfile(request):
    user = request.user
    form= UserForm(instance=request.user)

    if request.method == 'POST':
        form=UserForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('user-profile', pk=user.id )

    return render(request, 'base/update-profile.html', {'form':form})

@login_required(login_url='login')
def userSetting(request):
   
    return render(request, 'base/user-settings.html')
    

def topicPage (request):
    q= request.GET.get('q') if request.GET.get('q') != None else ''
    topics=Topic.objects.filter(
        Q(name__icontains=q )
    )

    context = {'topics':topics}

    return render(request, 'base/topics.html', context)
    

def activityPage(request):

    room_message = Message.objects.all()
    context= {'room_message':room_message}

    return render(request, 'base/activity.html', context)




def about(request):
    return render(request, 'base/about.html')