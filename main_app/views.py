from django.shortcuts import render, redirect
from django.utils import timezone
from django.http import HttpResponse, JsonResponse

import requests
import json
import uuid
import os
import boto3
import math

from django.views.decorators.csrf import csrf_exempt
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView

from django.urls import reverse_lazy, reverse
from .models import Profile, Comment, Photo

from .forms import ProfileForm

from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required 
from django.contrib.auth.mixins import LoginRequiredMixin 

from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt

# ---------------- Home ----------------------------


def home(request):
  return render(request, 'home.html')


def about(request):
  return render(request, 'about.html')




# ---------------- Sign-Up ------------------------


def signup(request):
  error_message = ''
  if request.method == 'POST':
    form = UserCreationForm(request.POST)
    if form.is_valid():
      user = form.save()
      login(request, user)
      return redirect('create_profile')
    else:
      error_message = 'Invalid sign up - try again!'
  form = UserCreationForm()
  context = {'form': form, 'error_message': error_message}
  return render(request, 'registration/signup.html', context)

@login_required
def profile(request):
  try:
    profile = Profile.objects.get(user=request.user)
    context = {'profile': profile}
    if profile:
        profile_form = ProfileForm(instance=profile)
        comments = Comment.objects.filter(user=request.user)
        context['profile_form']=profile_form
        context['comments']=comments
    return render(request, 'user/profile.html', context)
  except Profile.DoesNotExist:
    return redirect('create_profile')

#-------------Create Profile----------------


class ProfileCreate(CreateView):
  model = Profile
  template_name = 'user/create_profile.html'
  fields = ['age', 'gender', 'location', 'is_couch_potato', 'favorites']
  success_url = reverse_lazy('profile')  # Replace 'profile-detail' with your actual URL pattern

  def form_valid(self, form):
      print('form_valid being executed')
      form.instance.user = self.request.user
      return super().form_valid(form)


# -------------------- Matching Functions -------------------------------

def match(request):
   profile = Profile.objects.get(user=request.user)
   return render(request, 'user/match.html', {'profile':profile})

class ActivityUpdate(UpdateView):
  model = Profile
  template_name = 'user/update_activity.html'
  fields = ['is_couch_potato', 'chosen_activities']
  success_url = reverse_lazy('match')

  def form_valid(self, form):
      print('form_valid being executed')
      form.instance.user = self.request.user
      return super().form_valid(form)
  
  def get_success_url(self):
        return reverse('match')


# Load The Matching Page
@login_required
def my_match(request, latitude, longitude):
    profile = Profile.objects.get(user=request.user)
    profile.latitude = float(latitude)
    profile.longitude = float(longitude)
    profile.save()
    print(profile.id)
    return redirect (f'/find/{ profile.id }/')
    # find_match(request, profile.id)

def haversine(lat1, lon1, lat2, lon2):
  R = 6371
  dist_lat = math.radians(lat2 - lat1)
  dist_lon = math.radians(lon2 - lon1)
  a = math.sin(dist_lat / 2) * math.sin(dist_lat / 2) + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dist_lon / 2) * math.sin(dist_lon / 2)
  c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
  distance = R*c
  return distance

def find_match(request, profile_id):
  profile = Profile.objects.get(id=profile_id)
  user_latitude = profile.latitude
  user_longitude = profile.longitude
  user_chosen_activities = profile.chosen_activities
  active_profiles = Profile.objects.filter(is_couch_potato=True, chosen_activities__contains=user_chosen_activities).exclude(id=profile.id)
  matched_profiles = []
  matched_distance = [] 
  #Check if haversine distance is within a range (5.0km)
  for profile in active_profiles:
    distance = round(haversine(user_latitude, user_longitude, profile.latitude, profile.longitude), 1)  
    if distance < 8000.0:
      matched_profiles.append(profile)
      matched_distance.append(distance)
  print(matched_profiles)
  print(matched_distance)
  return render(request, 'user/my_matches.html', {
     'profile':profile, 
     'matched_profiles':matched_profiles, 
     'matched_distance':matched_distance, 
     'user_latitude':user_latitude, 
     'user_longitude':user_longitude, 
     })

def view_friend_profile(request, user_id):
  try:
    print(user_id)
    profile = Profile.objects.get(user=user_id)
    print(profile.user)
    context = {'profile': profile}
    if profile:
        # profile_form = ProfileForm(instance=profile)
        comments = Comment.objects.filter(user=user_id)
        # context['profile_form']=profile_form
        context['comments']=comments
        context['friend_profile']=profile
    return render(request, 'user/friends_profile.html', context)
  except Profile.DoesNotExist:
    return redirect('my_match')
  
# ---------------- Update Profile ------------------------
class ProfileUpdate(UpdateView):
  model = Profile
  template_name = 'user/update_profile.html'
  fields = ['gender', 'age', 'location', 'favorites']

  success_url = reverse_lazy('profile')

  def form_valid(self, form):
      print('form_valid being executed')
      form.instance.user = self.request.user
      return super().form_valid(form)
  
  def get_success_url(self):
        return reverse('profile')

# ---------------Comment Section --------------------


class CommentListView(LoginRequiredMixin, ListView):
    model = Comment
    template_name = 'user/profile.html'
    context_object_name = 'comments'
    ordering = ['-created_at']
    # Filter comments for the current user
    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)
        

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = self.get_queryset()
        return context  


class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    fields = ['content']
    template_name = 'user/create_comment.html'
    success_url = reverse_lazy('profile')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    
        
class CommentUpdateView(LoginRequiredMixin, UpdateView):
    model = Comment
    fields = ['content']
    template_name = 'user/edit_comment.html'
    success_url = reverse_lazy('profile')

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)

      
class CommentDeleteView(LoginRequiredMixin, DeleteView):
    model = Comment
    template_name = 'user/delete_comment.html'
    success_url = reverse_lazy('profile')

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)
    

@login_required
def add_photo(request, user_id):
  photo_file = request.FILES.get('photo_file', None)
  if photo_file:
    s3 = boto3.client('s3')
    key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
    try:
      bucket = os.environ['S3_BUCKET']
      s3.upload_fileobj(photo_file, bucket, key)
      url = f"{os.environ['S3_BASE_URL']}{bucket}/{key}"
      Photo.objects.create(url=url, user_id=user_id)
    except Exception as e:
      print('An error occurred uploading file to S3')
      print(e)
  return redirect('profile')