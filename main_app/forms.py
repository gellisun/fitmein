from django import forms
from django.forms import ModelForm
from .models import Profile, ACTIVITIES

class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['location', 'favorites']