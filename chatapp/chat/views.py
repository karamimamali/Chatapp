from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.views.decorators.csrf import csrf_protect
import logging
import json

from .models import User, ChatGroup

# Create your views here.
def index(request):
    return render(request, "chat/index.html")

def about(request):
    return render(request, "chat/about.html")

@csrf_protect
def create_room(request):
    if request.method == "GET":
        return render(request, "chat/create_room.html")

    try:
        data = json.loads(request.body.decode('utf-8'))
        roomName = data.get('roomName')
        roomPassword = data.get('roomPasword')

        group = ChatGroup(name=roomName, password=make_password(roomPassword))
        group.save()

        group.users.add(request.user)

        return redirect("room", room_name=roomName)

    except Exception as e:
        logging.error("Something went wrong:\n", repr(e))
    

@login_required
def room(request, room_name):
    return render(request, "chat/room.html", {"room_name":room_name,
        "username": request.user.username
    })

