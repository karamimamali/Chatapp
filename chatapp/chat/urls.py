from django.urls import path

from . import views

urlpatterns = [
    path("",views.index, name="index"),
    path("create_room/", views.create_room, name="create_room"),
    path("join_room/", views.join_room, name="join_room"),
    path("about/", views.about, name="about"),
    path("<str:room_name>/", views.room, name="room"),
]
