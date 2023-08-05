import os
from django.shortcuts import render
from .models import Profile, Badges

def home(request):
  return render(request, 'home.html')

def about(request):
  return render(request, 'about.html')
