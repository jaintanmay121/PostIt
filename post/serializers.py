from rest_framework import serializers
from post.models import Posts

from django.conf import settings 


class PostSerializer(serializers.Serializer): # Modelerializer):

    # class Meta:
    #     model = Posts
    #     fields = ('user', 'postTitle', 'post', 'likes', 'postDate')
    #     # fields = ('user', 'postTitle', 'post', 'likes.count()', 'postDate.date()')

    User = settings.AUTH_USER_MODEL 
    postTitle = serializers.CharField(max_length= 20)
    post = serializers.CharField(max_length=5000)
    likes = serializers.ManyRelatedField() #ManyToManyField(User, related_name='Like')
    postDate = serializers.DateTimeField(auto_now_add=True, null= True)
    