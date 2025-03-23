from django import forms
from .models import Post, Comment, User
from django.contrib.auth.forms import UserChangeForm

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title','text', 'location', 'category', 'pub_date', 'image')
        exlude = ('comment', 'author')
        
        widgets = {
            'pub_date': forms.DateInput(attrs={'type': 'date'}),
        }


class CommentForm(forms.ModelForm): 
    class Meta:
        model = Comment
        fields = ('text',)
        
        widgets = {
            'comment': forms.Textarea(attrs={'cols': 20, 'rows': 5}),
        }


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email']