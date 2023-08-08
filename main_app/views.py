from django.shortcuts import render, redirect
from django.utils import timezone
from django.http import HttpResponse
import requests
import json
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView

from .models import Matcher
from .forms import SignUpForm

from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required #  Login required for View Functions
from django.contrib.auth.mixins import LoginRequiredMixin #  Login required for Class-based Views

# ---------------- Home ----------------------------

def home(request):
  return render(request, 'home.html')

def about(request):
  return render(request, 'about.html')


# ---------------- 2-step Sign-Up ------------------------

def signup(request):
  error_message = ''
  if request.method == 'POST':
    form = UserCreationForm(request.POST)
    if form.is_valid():
      user = form.save()
      login(request, user)
      return redirect('profile_create')
    else:
      error_message = 'Invalid sign up - try again!'
  form = UserCreationForm()
  context = {'form': form, 'error_message': error_message}
  return render(request, 'registration/signup.html', context)

def signuptwo(request):
  try:
    profile = Profile.objects.get(user=request.user)
    profile_exists = True
  except Profile.DoesNotExist:
    profile = None
    profile_exists = False

  if request.method == 'POST':
    profile_form = ProfileForm(request.POST, instance=profile)
    if profile_form.is_valid():
      profile_form.save()
    else:
      new_profile = profile_form.save(commit=False)
      new_profile.user = request.user
      new_profile.save()
  else:
    if profile_exists:
      profile_form = ProfileForm(instance=profile)
    else:
      profile_form = ProfileForm()
  context = {'profile': profile, 'profile_form': profile_form,}
  return render(request, 'user/profile.html', context)

# class ProfileCreate(LoginRequiredMixin,CreateView):
#   model = Profile
#   fields = ['age', 'location']

  def form_valid(self, form):
    form.instance.user = self.request.user
    return super().form_valid(form)

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Log the user in after successful registration
            login(request, user)
            return redirect('profile')  # Replace 'home' with the URL name for your home page
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

# -------------------- User Area -------------------------------

@login_required
def profile(request, profile_id):
  print(profile_id)
  profile = Profile.objects.get(id=profile_id)
  return render(request, 'user/profile.html', {
    'profile': profile,
  })

@login_required
def match(request):
  print(request.user.id)
  ip = requests.get('https://api.ipify.org?format=json')
  ip_data = json.loads(ip.text)
  res = requests.get('http://ip-api.com/json/'+ip_data["ip"]) #get a json
  location_data_one = res.text #convert JSON to python dictionary
  location_data = json.loads(location_data_one) #loading location data one~
  if request.method == 'POST':
    latitude = request.POST.get('latitude')
    longitude = request.POST.get('longitude')

    profile = Profile.objects.get(user=request.user)
    profile.latitude = latitude
    profile.longitude = longitude
    profile.save()
    return HttpResponse(status=200)

  profile = Profile.objects.get(user=request.user)
  return render(request, 'user/match.html', {
    'data': location_data, 
    'ip': ip_data,
    'profile': profile
  })


# @login_required
# def profile(request):

#  try:
#     profile = Profile.objects.get(user=request.user)
#     profile_exists = True
#  except Profile.DoesNotExist:
#     profile = None
#     profile_exists = False

#  if request.method == 'POST':
#     profile_form = ProfileForm(request.POST, instance=profile)
#     if profile_form.is_valid():
#         profile_form.save()
#     else:
#         new_profile = profile_form.save(commit=False)
#         new_profile.user = request.user
#         new_profile.save()
#  else:
#     if profile_exists:
#       profile_form = ProfileForm(instance=profile)
#     else:
#       profile_form = ProfileForm()

#  context = {'profile': profile, 'profile_form': profile_form,}
#  return render(request, 'user/profile.html', context)
