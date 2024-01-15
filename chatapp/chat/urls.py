from django.urls import path

from . import views

urlpatterns = [
    path("", views.create_group, name="create_group"),
    path("about/", views.about, name="about"),
    path("<str:room_name>/", views.room, name="room"),
]
