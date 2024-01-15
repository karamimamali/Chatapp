from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.

def create_group(request):
    return render(request, "chat/create_group.html")

@login_required
def room(request, room_name):
    return render(request, "chat/room.html", {"room_name":room_name,
        "username": request.user.username
    })

def about(request):
    return render(request, "chat/about.html")