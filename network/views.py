import json
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.core.paginator import Paginator
from itertools import chain
from django.views.decorators.csrf import csrf_exempt
from .models import *


def index(request):
    Toweets = Post.objects.all().order_by('-PostCreatedAt')
    p = Paginator(Toweets, 10)
    page_number = request.GET.get('page')
    page_obj = p.get_page(page_number)
    return render(request, "network/index.html", {
        'page_obj': page_obj,
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
    
def createToweet(request):
    if request.method == 'POST':
        newPost = Post()
        newPost.PostCreator = request.user
        newPost.PostContent = request.POST['toweetbody']
        newPost.save()
    return index(request)

def showUserInfo(request, name):

    userid = User.objects.get(username=name).id
    user = User.objects.get(username=name)
    toweets = Post.objects.filter(PostCreator_id = userid).order_by('-PostCreatedAt')
    p = Paginator(toweets, 10)
    page_number = request.GET.get('page')
    page_obj = p.get_page(page_number)
    context = {
        "currentuser" : user,
        "user" : request.user,
        "page_obj": page_obj,
        "userfollowing" : user.following.all(),
        "userfollowers" : user.followers.all(),
        "followerscount" : user.followers.count(),
        "followingcount" : user.following.count()
    }
    return render(request, "network/userinfo.html", context)

def followuser(request, name):
    u1 = User.objects.get(username=name)
    a1 = User.objects.get(username=request.user)
    if a1 in u1.followers.all():
        a1.following.remove(u1)
        u1.followers.remove(a1)
    else:
        a1.following.add(u1)
        u1.followers.add(a1)
    return HttpResponseRedirect(reverse('userinfo', args=(u1,)))

def following(request):
    u1 = request.user
    # Creating new set toweets to get all following
    toweets = set()
    u1.all = User.objects.get(username=u1).following.all()
    for i in u1.all:
        # Using For loop to add each following persons toweets to toweets set.
        toweets.add(Post.objects.filter(PostCreator_id = i.id).order_by('-PostCreatedAt'))
    followtoweets = []
    # Using for loop to add toweets to followtoweets
    for i in toweets:
        for j in i:
            followtoweets.append(j)
    p = Paginator(followtoweets, 10)
    page_number = request.GET.get('page')
    page_obj = p.get_page(page_number)
    context = {
        "currentuser": u1,
        'page_obj': page_obj
    }
    return render(request, "network/following.html", context)

@csrf_exempt
def changeToweet(request, id):

    if request.user.is_authenticated:
        current_user = request.user
    else:
        return HttpResponse("You must be logged in to try to do that.")

    # Update whether email is read or should be archived
    if request.method == "PUT":
        toweet = Post.objects.get(id=id)
        if toweet.PostCreator_id == current_user.id:
            data = json.loads(request.body)
            newToweetContent = data.get("newToweetContent")
            toweet.PostContent = newToweetContent
            toweet.save()
            return JsonResponse(toweet.serialize())
        else:
            return HttpResponse("Access denied.")
    else:
        return HttpResponse("Access denied.")
        
@csrf_exempt
def likeToweet(request, id):
    if request.user.is_authenticated:
        if request.method == "PUT":
            toweet = Post.objects.get(id=id)
            data = json.loads(request.body)
            likeStatus = data.get("PostLikes")
            if likeStatus == True:
                toweet.PostLikes += 1
            else:
                toweet.PostLikes -= 1
            toweet.save()
            return JsonResponse(toweet.serialize())
    else:
        return HttpResponse("You must be logged in to do that.")
        
            






