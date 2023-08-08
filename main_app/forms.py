from django import forms
from django.forms import ModelForm
from django import forms
from .models import Profile, Comment

class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['location', 'age', 'gender', 'is_couch_potato', 'favorites']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
