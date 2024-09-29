from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .models import Room, Topic, Message, Profile
from .forms import RoomForm, UserForm,ProfileForm
from django.contrib.auth.forms import UserCreationForm

def loginPage(request):
    page = 'login'
    if request.user.is_authenticated:
        messages.error(request, 'you are already logged in')
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')
        print(username, password)
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'User does not exist')

        user = authenticate(request, username=username, password=password)
        print(user)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username or password does not exist')
    context = {'page': page}
    return render(request, 'base/login_register.html', context)


def logoutUser(request):
    logout(request)
    return redirect('home')



def registerPage(request):
    userForm = UserCreationForm()
    if request.method == 'POST':
        userForm = UserCreationForm(request.POST)
        if userForm.is_valid():
            user = userForm.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Something went wrong!!")

    context = {'form': userForm, }
    return render(request, 'base/login_register.html', context)

def home(request):
    query = request.GET.get('query') if request.GET.get('query') != None else ''
    rooms = Room.objects.filter(Q(topic__name__icontains=query)| Q(name__icontains=query) | Q(description__icontains=query))
    room_count = rooms.count()
    topics = Topic.objects.all()[0:5]
    
    conversations = Message.objects.filter(Q(room__topic__name__icontains=query))
    context = {'rooms': rooms, 'topics': topics, 'room_count': room_count, 'conversations': conversations}
    return render(request, 'base/home.html', context)


def rooms(request, pk=None):
    room = Room.objects.get(id=pk)
    conversations = room.message_set.all()
    participants = room.participants.all()
    print(participants)
    if request.method == 'POST':
        message = Message.objects.create(
            user = request.user,
            room = room,
            body = request.POST.get('conversation')
        )
        room.participants.add(request.user)
        return redirect('rooms', pk=room.id)
        

    context = {'room': room, 'conversations': conversations, 'participants': participants}
    return render(request, 'base/rooms.html', context)


    

@login_required(login_url='login')
def newRoom(request):
    page = 'create'
    form = RoomForm()
    topics = Topic.objects.all()
    if request.method == 'POST':
        topic = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic)
        Room.objects.create(
            host = request.user,
            topic = topic,
            name = request.POST.get('name'),
            description = request.POST.get('description'),
        )
        return redirect('home')


    context = {'form': form, 'topics': topics, 'page': page}
    return render(request, 'base/new_room.html', context)

@login_required(login_url='login')
def editRoom(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    topics = Topic.objects.all()

    if request.user != room.host:
        messages.error(request, 'you cant edit that!!')
        return redirect('home')
    if request.method == 'POST':
        topic = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic)
        room.name = request.POST.get('name')
        room.topic = topic
        room.description = request.POST.get('description')
        room.save()
        return redirect('home')
        
    context = {'form': form, 'topics': topics, 'room': room}
    return render(request, 'base/new_room.html', context)


@login_required(login_url='login')
def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)
    if request.user != room.host:
        messages.error(request, 'you cant delete that!!')
        return redirect('home')
    if request.method == 'POST':
        room.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj': room})

def deleteMessage(request, pk):
    message = Message.objects.get(id=pk)
    room = Room.objects.get(id=message.room.id)
    print(room)
    if request.user != message.user:
        messages.error(request, 'you cant delete that!!')
        return redirect('rooms', pk=room.id)
    if request.method == 'POST':
        message.delete()
        return redirect('rooms', pk=room.id)
    return render(request, 'base/delete.html', {'obj': message})




def userProfile(request, pk):
    user = User.objects.get(id=pk)
    rooms = user.room_set.all()
    conversations = user.message_set.all()
    topics = Topic.objects.all()
    profile = Profile.objects.get(user=user)
    context = {'user': user, 'rooms': rooms, 'conversations': conversations, 'topics': topics, 'profile': profile}
    return render(request, 'base/user_profile.html', context)


def updateProfile(request):
    user = request.user
    profile, created = Profile.objects.get_or_create(user=user)
    form = UserForm( instance=user)
    profileForm = ProfileForm(instance=profile)
    if request.method == 'POST':
        form = UserForm(request.POST, instance=user)
        profileForm = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid:
            form.save()
        if profileForm.is_valid:
            profileForm.save()

        return redirect('user_profile', pk=user.id)
    context = {'form':form,'profileForm': profileForm}
    return render(request, 'base/update_profile.html', context)


def topicsPage(request):
    query = request.GET.get('query') if request.GET.get('query') != None else ''
    topics = Topic.objects.filter(name__icontains=query)
    return render(request, 'base/topics.html',{'topics': topics})

def activityPage(request): 
    conversations = Message.objects.all()
    return render(request, 'base/activity.html', {'conversations': conversations})