# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import redirect, render
from django.core.validators import validate_email
from django.core.exceptions import ObjectDoesNotExist
from chat.forms import MsgForm, NewRoomForm, SignupForm, LoginForm
from chat.models import Message, Room
from django.contrib import messages
from django.contrib.auth import get_user_model, login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.forms import ValidationError
from friendship.models import Friend, FriendshipRequest

User=get_user_model()

# Create your views here.
def home(request):
    if not request.user.is_authenticated:
        if request.method=='POST':
            form=LoginForm(request.POST)
            if form.is_valid():
                email=form.cleaned_data['email']
                password=form.cleaned_data['password']
                user=authenticate(email=email, password=password)
                if user:
                    login(request, user)
                    return redirect('/')
        form=LoginForm()
        return render(request, 'chat/home.html', {'form': form})
    else:
        rooms=Room.objects.all()
        pms = Friend.objects.unread_requests(user=request.user)
        pms=len(pms)
        return render(request, 'chat/home.html', {'rooms': rooms, 'pms': pms})

@login_required(login_url='/')
def new_room(request):
    if request.method=='POST':
        form=NewRoomForm(request.user, request.POST)
        if form.is_valid():
            room=form.save()
            return redirect(room.get_absolute_url())
    form=NewRoomForm(request.user)
    return render(request, 'chat/new_room.html', {'form': form})

@login_required(login_url='/')
def find_friends(request):
    user=None
    if 'email' in request.GET:
        try:
            validate_email(request.GET['email'])
        except ValidationError:
            messages.error(request, 'Not a valid email')
        try:
            user=User.objects.get(email=request.GET['email'])
        except ObjectDoesNotExist:
            messages.error(request, 'No result')
    if 'invite' in request.GET:
        invitee=User.objects.get(id=request.GET['invite'])
        msg=request.user.first_name + '(' + request.user.email + ') would like to connect with you.'
        Friend.objects.add_friend(request.user, invitee, message=msg)
        user=None
        messages.success(request, 'Invite sent to ' + invitee.first_name + '!')
    return render(request, 'chat/find_friends.html', {'friend': user})

@login_required(login_url='/')
def pm(request):
    if 'accept' in request.GET:
        f=FriendshipRequest.objects.get(pk=request.GET['accept'])
        f.accept()
    if 'decline' in request.GET:
        f = FriendshipRequest.objects.get(pk=request.GET['decline'])
        f.reject()
        f.delete()
    pms=Friend.objects.unread_requests(user=request.user)
    return render(request, 'chat/messages.html', {'pms': pms})

def signup(request):
    if request.method=='POST':
        form=SignupForm(request.POST)
        if form.is_valid():
            user=form.save()
            login(request, user)
            return redirect('/')
    else:
        form=SignupForm()
    return render(request, 'chat/signup.html', {'form': form})

def log_out(request):
    logout(request)
    return redirect('/')

@login_required(login_url='/')
def chat(request, room_id):
    try:
        room=Room.objects.get(title=room_id)
    except ObjectDoesNotExist:
        return redirect('/')
    user = request.user
    group=Group.objects.get(id=room.group_id)
    if not group in user.groups.all():
        return redirect('/')
    if request.method=='POST':
        form=MsgForm(request.POST)
        if form.is_valid():
            msg=form.save(author=user, room=room)
    form=MsgForm()
    messages=Message.objects.filter(room=room).order_by('pub_date')
    return render(request, 'chat/chat.html', {'room': room, 'form': form, 'messages': messages})