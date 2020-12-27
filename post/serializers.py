from rest_framework import serializers
from post.models import Posts

class PostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Posts
        fields = ('user', 'postTitle', 'post', 'likes', 'postDate')