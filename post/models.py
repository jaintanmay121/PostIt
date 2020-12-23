from django.db import models
from django import forms
from django.contrib.auth.models import User
from django.conf import settings 

User = settings.AUTH_USER_MODEL 

# New Post model
class Posts(models.Model):
    user = models.ForeignKey(User, 
                        default = 1, 
                        null = True,  
                        on_delete = models.SET_NULL 
                        )
    postTitle = models.CharField(max_length= 20)
    post = models.CharField(max_length=5000)
    likes = models.ManyToManyField(User, related_name='Like')
    postDate = models.DateTimeField(auto_now_add=True, null= True)

    def number_of_likes(self):
        return self.likes.count()

    def __str__(self):
        return self.postTitle