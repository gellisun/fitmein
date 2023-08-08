from django.forms import ModelForm
from .models import CustomUser
from django import forms
from django.contrib.auth.forms import UserCreationForm

# class ProfileForm(ModelForm):
#     class Meta:
#         model = Profile
#         fields = ['location', 'age', 'gender', 'is_couch_potato', 'favorites']

class SignUpForm(UserCreationForm):
    age = forms.IntegerField(label='Age', required=False)
    gender = forms.CharField(max_length=10, label='Gender', required=False)
    city = forms.CharField(max_length=100, label='City', required=False)

    class Meta:
        model = CustomUser
        fields = ('username', 'password1', 'password2', 'first_name', 'last_name', 'age', 'gender', 'city')