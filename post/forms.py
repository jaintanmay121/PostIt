from django import forms
from .models import Posts
# from django.contrib.auth.models import User

class PostForm(forms.ModelForm):
  class Meta:
    model = Posts
    fields = ('postTitle', 'post')