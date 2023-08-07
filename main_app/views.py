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

def signup(request):
  error_message = ''
  if request.method == 'POST':
    form = UserCreationForm(request.POST)
    if form.is_valid():
      user = form.save()
      login(request, user)
      return redirect('profile')
    else:
      error_message = 'Invalid sign up - try again!'
  form = UserCreationForm()
  context = {'form': form, 'error_message': error_message}
  return render(request, 'registration/signup.html', context)