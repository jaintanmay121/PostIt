from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Posts
from django.contrib.auth.decorators import login_required
from .forms import PostForm
import requests
import json
import time

from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import PostSerializer

@api_view(['GET'])
def post_collection(request):
    if request.method == 'GET':
        posts = Posts.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)


@api_view(['GET'])
def post_element(request, pk):
    try:
        post = Posts.objects.get(pk=pk)
    except Posts.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = PostSerializer(post)
        return Response(serializer.data)








def getQuote():
    resp = requests.get('https://api.quotable.io/random')
    quote = json.loads(resp.text)["content"]
    return quote


# Function to log into the system
def userLogin(request):
    if request.user.is_authenticated:
        time.sleep(0.01)
        messages.info(request, "Already logged into an account.")
        return redirect('/feed/')
    quote = getQuote()
    if request.method == 'POST':
        # Verifies the credentials
        form = AuthenticationForm(request=request, data=request.POST)
        # If valid
        if form.is_valid():
            # Get credentials
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                time.sleep(0.01)
                login(request, user)
                # Redirect to Feeds
                return redirect('/feed/')

            else:
                messages.error(request, "Invalid username or password.")
        # If not valid
        else:
            print("\n\nInvalid username or password.\n\n")

            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()
    return render(request=request,
                  template_name="post/login.html",
                  context={"form": form, "quote": quote})


# Function to Sign Up
def register(request):
    
    if request.user.is_authenticated:
        time.sleep(0.01)
        messages.info(request, "Already logged into an account.")
        return redirect('/feed/')

    quote = getQuote()
    if request.method == 'POST':
        # Get the credentials for signing up
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        # Updating to table
        user = User.objects.create_user(username, email, password)
        # Saving the changes
        user.save()
        # Redirect to login page
        return redirect('/login/')

    return render(request, 'post/register.html', context={"quote": quote})


# Function to logout
def userLogout(request):
    logout(request)
    return redirect("/login")


# Function for the main index page
@login_required(login_url='/login/')
def index(request):
    # Get a quote for right column
    quote = getQuote()
    # Load all posts
    posts = Posts.objects.all()
    
    # Get details for the posts
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            time.sleep(0.01)
            return redirect('/feed/')

    else:
        form = PostForm

    return render(request,
                  'post/index.html',
                  context={"name": request.user,
                           "posts": posts[::-1],
                           "form": form,
                           "Quote": quote
                           })


# Function to Delete a Post
@login_required(login_url='/login/')
def deletePost(request, pk):
    # Get the post as instance
    post = get_object_or_404(Posts, pk=pk)

    if request.method == 'POST':
        # Delete the post
        post.delete()
        time.sleep(0.01)
        return redirect('/feed/')

    return render(request)


def Like(request, pk):
    post = get_object_or_404(Posts, pk=pk)

    if request.method == 'POST':
        if post.likes.filter(id=request.user.id).exists():
            post.likes.remove(request.user)
        else:
            post.likes.add(request.user)
        return redirect('/feed/')

    return render(request)
