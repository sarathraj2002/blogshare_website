
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile,BlogPost,Comment

class UserRegisterForm(UserCreationForm):
    # password=forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model=User
        fields=['username','first_name','last_name','email']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }


class ProfileForm(forms.ModelForm):
    class Meta:
        model=Profile
        fields=['contact','profile_pic']
        widgets = {
            'contact': forms.TextInput(attrs={'class': 'form-control'}),
            'profile_pic': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

class BlogPostForm(forms.ModelForm):
    class Meta:
        model=BlogPost
        fields=['title','content','image']

class CommentForm(forms.ModelForm):
    class Meta:
        model=Comment
        fields=['content']