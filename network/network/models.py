from email.policy import default
from pyexpat import model
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author')
    content = models.CharField(max_length=250)
    timestamp = models.DateTimeField(auto_now_add=True)
    liked = models.ManyToManyField(User, default=None, blank=True, related_name='likes')
    
    def __str__(self):
        return f"{self.user.username} {self.timestamp} {self.content}"

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    def __str__(self):
        return(self.post)

class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='userFollowers')
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='userFollowing')

    def __str__(self):
        return (self.profile)