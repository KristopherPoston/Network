from venv import logger
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
import json
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import User, Post
from django.contrib import messages


def index(request):
    return render(request, "network/index.html")


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

def createPostViewPage(request):
    return render(request, "network/createPost.html")

def createPostModel(request):
    if request.method == "POST":
        postBody = request.POST.get('postBody')
        timestamp = request.POST.get('timeStamp')

        
        user = User.objects.get(username=request.user.username)
        newPost = Post(user=user, body=postBody, timestamp=timestamp)
        newPost.save()

        
        return redirect('allPosts')
        
    

def allPosts(request):
    posts = Post.objects.all().order_by('-timestamp')  
    paginator = Paginator(posts, 4) 
    page_number = request.GET.get('page')  
    page_object = paginator.get_page(page_number)  

    return render(request, "network/allPosts.html", {
        "page_object": page_object  
    })

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
    
    
def profileView(request, username):

    user = get_object_or_404(User, username=username)
    current_user_username = request.user.username
    
    
    if not username:
        return redirect("index")

    following_users = user.following.all()
    followers = user.followers.all()
    following_count = following_users.count()
    followers_count = followers.count()
    userPosts = Post.objects.filter(user=user)
    is_following = followers.filter(username=current_user_username).exists()

    

    if request.method == "GET":
        return render(request, "network/profile.html", {
            'user': user,
            'userPosts': userPosts,
            'following_count': following_count,
            'followers_count': followers_count,
            'is_following': is_following  
        })
    
   #what are some things i need to do paginate the posts
   #



    


def followingView(request):
    current_userName = request.user.username
    current_user = User.objects.get(username=current_userName)

    following_users = current_user.following.all()
    posts = Post.objects.filter(user__in=following_users)

    return render(request, 'network/following.html', {
        'posts': posts
    })

@require_POST
def editPost(request):
    if request.method == "POST":
        data = json.loads(request.body)
        postID = data.get("postID")
        postBody = data.get("postBody")

        post = Post.objects.get(id = postID)
        post.body = postBody
        post.save()

        return JsonResponse({"message": "Post updated successfully"})


@require_POST
def followUser(request):
    if request.method == "POST":
        data = json.loads(request.body)
        user = User.objects.get(username = data.get("userProfile"))

        current_userName = request.user.username


        followStatus = data.get("followStatus")
        current_user = User.objects.get(username=current_userName)


        if followStatus == "Unfollow":
            user.followers.remove(current_user)
            user.save()
            followers = user.followers.count()
            followStatus = "Follow"
            current_user.following.remove(user)
            current_user.save()
            return JsonResponse({"followers": followers, "followStatus": followStatus})
        
        if followStatus == "Follow":
            user.followers.add(current_user)
            user.save()
            followers = user.followers.count()
            followStatus = "Unfollow"
            current_user.following.add(user)
            current_user.save()
            return JsonResponse({"followers": followers, "followStatus": followStatus})
        
        return JsonResponse({"error": "Invalid follow status"}, status=400)

    return JsonResponse({"error": "Invalid request method"}, status=400)

        

    #do nothing for now

from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.shortcuts import get_object_or_404
from .models import Post, User
import json

@require_POST
def incrementLikes(request):
    try:
        data = json.loads(request.body)
        logger.debug(f"Received data: {data}")
        username = data.get("user")
        postID = int(data.get("postID"))
        changebutton = ""

        post = get_object_or_404(Post, id=postID)
        user = get_object_or_404(User, username=username)

        Disliked = user.disliked_posts.filter(id=postID).exists()
        Liked = user.liked_posts.filter(id=postID).exists()

        if Disliked:
            user.disliked_posts.remove(post)
            post.dislikes -= 1
            post.likes += 1
            user.liked_posts.add(post)
            changebutton = "True"

        if Liked:
            user.liked_posts.remove(post)
            post.likes -= 1
            post.dislikes += 1
            user.disliked_posts.add(post)

        if not Liked and not Disliked:
            user.liked_posts.add(post)
            post.likes += 1

        post.save()
        user.save()

        return JsonResponse({'likes': post.likes, 'changebutton': changebutton, 'dislikes': post.dislikes})
    except Post.DoesNotExist:
        return JsonResponse({'error': 'Post not found'}, status=404)
    except User.DoesNotExist:
        return JsonResponse({'error': 'User not found'}, status=404)
    except Exception as e:
        logger.error(f"Error processing request: {e}")
        return JsonResponse({'error': str(e)}, status=500)

@require_POST
def incrementDislikes(request):
    try:
        data = json.loads(request.body)
        username = data.get("user")
        postID = int(data.get("postID"))
        changeLikeButton = ""

        user = get_object_or_404(User, username=username)
        post = get_object_or_404(Post, id=postID)


        Disliked = user.disliked_posts.filter(id=postID).exists()
        Liked = user.liked_posts.filter(id=postID).exists()


        if Disliked:
            user.disliked_posts.remove(post)
            changeLikeButton = "True"
            post.dislikes -= 1

        if Liked: #when the user has liked the post, instead of decrementing the likes adding incrementing the dislikes, it just increments the dislikes
            post.likes -= 1
            user.liked_posts.remove(post)
            user.disliked_posts.add(post)
            post.dislikes += 1
            changeLikeButton = "True"

            if post.dislikes == 0:
                post.dislikes = 0

        if (not Liked) and (not Disliked):
            user.disliked_posts.add(post)
            post.dislikes += 1

        if post.dislikes < 0:
            post.dislikes = 0

        

        post.save()
        user.save()

        return JsonResponse({'dislikes': post.dislikes, 'likes': post.likes, 'changeLikeButton': changeLikeButton})
    except Post.DoesNotExist:
        return JsonResponse({'error': 'Post not found'}, status=404)
    except User.DoesNotExist:
        return JsonResponse({'error': 'User not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

 



