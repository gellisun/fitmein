from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView

from .models import Profile, Badges, User
from .forms import ProfileForm

from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required #  Login required for View Functions
from django.contrib.auth.mixins import LoginRequiredMixin #  Login required for Class-based Views

def home(request):
  return render(request, 'home.html')

def about(request):
  return render(request, 'about.html')


@login_required
def profile(request):
  profile, created = Profile.objects.get_or_create(user=request.user)
  if request.method == 'POST':
    profile_form = ProfileForm(request.POST, instance=profile)
    if profile_form.is_valid():
      profile_form.save()
  else:
    profile_form = ProfileForm(instance=profile)

  context = {'profile': profile, 'profile_form': profile_form,}
  return render(request, 'user/profile.html', context)

def signup(request):
  error_message = ''
  # profile, created = Profile.objects.get_or_create(user=request.user)
  if request.method == 'POST':
    # profile_form = ProfileForm(request.POST, instance=profile)
    form = UserCreationForm(request.POST)
    # if form.is_valid() and profile_form.is_valid():
    if form.is_valid():
      user = form.save()
      # profile_form.save()
      login(request, user)
      return redirect('profile')
    else:
      error_message = 'Invalid sign up - try again!'
      profile_form = ProfileForm()
  form = UserCreationForm()
  context = {'form': form, 'error_message': error_message,}
  return render(request, 'registration/signup.html', context)

   

  