from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass
    disliked_posts = models.ManyToManyField('Post', blank=True, related_name="disliked_posts")
    liked_posts = models.ManyToManyField('Post', blank=True, related_name="liked_posts")
    following = models.ManyToManyField('User', blank=True, related_name="followers")
    
    def __str__(self):
        return self.username


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    body = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    likes = models.IntegerField(default=0)
    dislikes = models.IntegerField(default=0)
    liked_by = models.ManyToManyField(User, related_name="liked_post", blank=True)
    disliked_by = models.ManyToManyField(User, related_name="disliked_post", blank=True)


    def __str__(self):
        return f"Post by {self.user.username} at {self.timestamp} "
    