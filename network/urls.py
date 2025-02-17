
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("createPostViewPage", views.createPostViewPage, name = "createPostViewPage"),
    path("createPostModel", views.createPostModel, name = "createPostModel"),
    path("allPosts", views.allPosts, name = "allPosts"),
    path("<str:username>/", views.profileView, name="profileView"),
    path("followingView", views.followingView, name = "followingView"),
    path("incrementLikes", views.incrementLikes, name = "incrementLikes"),
    path("incrementDislikes", views.incrementDislikes, name="incrementDislikes"),
    path("followUser", views.followUser, name="followUser"),
    path("editPost", views.editPost, name = "editPost")
]
