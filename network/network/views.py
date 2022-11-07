from gc import get_objects
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required


from .models import User, Profile, Post


def index(request):
    
        posts = Post.objects.all().order_by('id').reverse()
        return render(request, "network/index.html",{
            "posts": posts
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

@login_required
def save_post(request):
    if request.method == "POST":
        form_content = Post(content=request.POST['content'])
        
        post = Post.objects.create(content=form_content,user=request.user)
        post.save()
        return HttpResponse({
            "success": "post created",
        }, status=201)

    return index(request)


def profile(request,username):
    if request.method == 'GET':
        current_user = request.user
        user_data = get_object_or_404(User,username=username)
        posts = Post.objects.filter(user=user_data).order_by('id').reverse()
        follower = Profile.objects.filter(user=user_data)
        following = Profile.objects.filter(follower=user_data)
        return render(request, "network/profile.html",{
            "posts": posts,
            "user_data": user_data,
            "totalFollowers": len(follower),
            "totalFollowing": len(following)

        })
    else: 
        current_user = request.user
        user_data = get_object_or_404(User,username=username)
        posts = Post.objects.filter(user=user_data).order_by('id').reverse()
        followingUser = Profile.objects.filter(follower=request.user, user=user_data)

        if not followingUser:
            following = Profile.objects.create(user=user_data, follower=current_user)
            #following = Profile(user=user_data, follower=current_user)
            following.save()
            followingUser = Profile.objects.filter(follower=current_user, user=user_data)
            return render(request, 'network/profile.html',{
                "posts": posts,
                "user_data": user_data,
                "followingUser": followingUser
            })
        else:
            followingUser.delete()
            return render(request, 'network/profile.html',{
                "posts": posts,
                "user_data": user_data,
                "followingUser": followingUser
            })




def newPost(request, user_id):
    if request.method == "POST":
        #user = User.objects.get(pk=user_id)
        user = get_object_or_404(User, id=user_id)
        post_content = request.POST["textarea"]
        post = Post.objects.create(content=post_content,user=user)
        post.save()
        return render(request, "network/index.html", {
                "message": "Posted."
            })

def following(request, user_id):
    user = User.objects.get(pk=user_id)
    followers = Profile.objects.filter(follower=user)
    posts = Post.objects.all().order_by('id').reverse()
    post_list = []

    if not followers:
        return render(request, 'network/following.html',{
            "message": "no followers"
        })


    for post in posts:
        for follower in followers:
            if follower.user == post.user:
                post_list.append(post)
    
    
    return render(request, 'network/following.html',{
        'posts': post_list
    })