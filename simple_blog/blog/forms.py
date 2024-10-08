from django import forms
from .models import Post, Comment
from django.contrib.auth.models import User


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content','author']

    author = forms.ModelChoiceField(queryset=User.objects.all(), required=True, label="Select Author")



class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
    
    user = forms.ModelChoiceField(queryset=User.objects.all(), required=True, empty_label="Select a user")



class UpdateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content']
