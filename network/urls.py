
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("createToweet", views.createToweet, name="createToweet"),
    path("user/<str:name>", views.showUserInfo, name="userinfo"),
    path("following", views.following, name="following"),
    path("<str:name>", views.followuser, name="followuser"),

    # API Routes
    path("Post/<int:id>", views.likeToweet, name="likeToweet"),
    path("Post/update/<int:id>", views.changeToweet, name="changeToweet")
]
