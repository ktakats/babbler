# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request, 'chat/home.html')

def chat(request, room):
    return render(request, 'chat/chat.html')