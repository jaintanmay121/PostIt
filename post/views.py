from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
# from rest_framework import serializers
from rest_framework.response import Response
from .models import Posts
from django.contrib.auth.decorators import login_required
import requests
import json
import time


# from django.http import HttpResponse
# from rest_framework.decorators import api_view
# from rest_framework.response import Response
# from .serializers import PostSerializer


# @api_view(['GET'])
# def post_collection(request):
#     if request.method == 'GET':
#         posts = Posts.objects.all()
#         print("\n\n\n\n\n\n")
#         data = []
#         for i in posts:
#             # print(i.user, type(i.user))
#             temp = {'user': i.user, 'postTitle': i.postTitle, 'post': i.post,
#                     'likes': i.likes.count(), 'postDate': i.postDate.date()}
#             data.append(temp)
#         serializer = PostSerializer(data, many=True)
#         # serializer = PostSerializer(posts, many=True)
#         return Response(serializer)


# @api_view(['GET'])
# def post_element(request, pk):

#     print(f"\n\n{pk}\n\n")
#     try:
#         post = Posts.objects.get(pk=pk)
#         data = {'user': post.user,
#                 'postTitle': post.postTitle,
#                 'post': post.post,
#                 'likes': post.likes.count(),
#                 'postDate': post.postDate.date()
#                 }
#     except Posts.DoesNotExist:
#         return HttpResponse(status=404)

#     if request.method == 'GET':
#         serializer = PostSerializer(data=data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)#, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors)#, status=status.HTTP_400_BAD_REQUEST)
#         # serializer = PostSerializer(data)#post)
#         # return Response(serializer.data)
from django.http import JsonResponse
from rest_framework.decorators import api_view
from django.contrib.auth.models import User


@api_view(["GET"])
def sendAll(request):
    posts = Posts.objects.all()
    content = []
    for post in posts:
        data = {"user": post.user.username,
                'postTitle': post.postTitle,
                'post': post.post,
                'likes': post.likes.count(),
                'postDate': post.postDate.date()
                }
        content.append(data)
    return Response(content)


@api_view(["GET"])
def sendUser(request, username):

    try:
        pk = User.objects.get(username__iexact=username).pk
    except User.DoesNotExist:
        from rest_framework import exceptions
        raise exceptions.NotFound(detail="User Does Not Exist! Try checking the username.")

    posts = Posts.objects.filter(user=pk)
    content = {}
    for post in posts:
        data = {'postTitle': post.postTitle,
                'post': post.post,
                'likes': post.likes.count(),
                'postDate': post.postDate.date()
                }

        content[post.user.username] = data
    return Response(content)


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
        return redirect('/')#login/')

    return render(request, 'post/register.html', context={"quote": quote})


# Function to logout
def userLogout(request):
    logout(request)
    return redirect("/")#login")


# Function for the main index page
@login_required(login_url='/')#login/')
def index(request):
    from .forms import PostForm
    # Get a quote for right column
    quote = getQuote()
    # Load all posts
    posts = Posts.objects.all().order_by('-postDate')

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
                           "posts": posts,
                           "form": form,
                           "Quote": quote
                           })


# Function to Delete a Post
@login_required(login_url='/')#login/')
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
