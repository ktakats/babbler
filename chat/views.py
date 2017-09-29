# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import redirect, render
from django.core.exceptions import ObjectDoesNotExist
from chat.forms import MsgForm, NewRoomForm, SignupForm, LoginForm
from chat.models import Message, Room
from django.contrib.auth import get_user_model, login, logout, authenticate
from django.contrib.auth.decorators import login_required

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
        if request.method=='POST':
            form=NewRoomForm(request.POST)
            if form.is_valid():
                room=form.save()
                return redirect(room.get_absolute_url())
        form=NewRoomForm()
        rooms=Room.objects.all()
        return render(request, 'chat/home.html', {'form': form, 'rooms': rooms})

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
    if request.method=='POST':
        form=MsgForm(request.POST)
        if form.is_valid():
            user=request.user
            msg=form.save(author=user, room=room)
    form=MsgForm()
    messages=Message.objects.filter(room=room).order_by('pub_date')
    return render(request, 'chat/chat.html', {'room': room, 'form': form, 'messages': messages})