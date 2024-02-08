from django.urls import path

from . import views

urlpatterns = [
    path("", views.create_user, name="create_user"),
    path("login", views.login, name="login"),
    path("register", views.register, name="register"),
    path("logout", views.logout, name="logout"),
]
