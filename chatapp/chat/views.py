from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password, check_password
from django.views.decorators.csrf import csrf_protect
from django.http import JsonResponse
from django.db import IntegrityError
from django.urls import reverse
import logging
import json

from .models import User, ChatGroup

# Create your views here.
def index(request):
    return render(request, "chat/index.html")

def about(request):
    return render(request, "chat/about.html")

@login_required
def create_room(request):
    if request.method == "GET":
        return render(request, "chat/create_room.html")
    try:
        if request.method == "POST":
            data = json.loads(request.body.decode('utf-8'))
            room_name = data.get('roomName')
            room_password = data.get('roomPassword')

            group = ChatGroup(name=room_name, password=make_password(room_password))
            group.save()

            if request.user.is_authenticated:
                group.users.add(request.user)

            response_data = {'redirect': reverse('room', args=[room_name])}
            return JsonResponse(response_data)

    except IntegrityError:
        response_data = {'error': 'This room name is taken. Please choose a different one.'}
        return JsonResponse(response_data, status=400)

    except Exception as e:
        logging.error("Something went wrong:\n", repr(e))
        response_data = {'error': 'An error occurred while creating the room.'}
        return JsonResponse(response_data, status=500)


@login_required
def join_room(request):
    if request.method == "GET":
        return render(request, "chat/join_room.html")

    try:
        data = json.loads(request.body.decode('utf-8'))
        room_name = data.get('roomName')
        room_password = data.get('roomPassword')

        group = ChatGroup.objects.filter(name=room_name).first()

        if group and check_password(room_password, group.password):
            response_data = {'redirect': reverse('room', args=[room_name])}
            return JsonResponse(response_data)
        else:
            error_message = "Invalid room name or password"
            field_errors = {'roomName': error_message, 'roomPassword': error_message}
            return JsonResponse({'error': field_errors}, status=400)

    except Exception:
        response_data = {'error': 'Something went wrong'}
        return JsonResponse(response_data, status=500)


@login_required
def room(request, room_name):

    group = ChatGroup.objects.filter(name=room_name).first()

    if group and request.user not in group.users.all():
        return redirect('join_room')
    
    return render(request, "chat/room.html", {"room_name":room_name,
        "username": request.user.username
    })

