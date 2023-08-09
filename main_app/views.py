from django.shortcuts import render, redirect
from django.utils import timezone
from django.http import HttpResponse, JsonResponse
import requests
import json
import uuid
import os
import boto3
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.urls import reverse_lazy
from django.utils import timezone

from .models import Profile, Badges, User, Comment, Photo

from .forms import ProfileForm, CommentForm


from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required #  Login required for View Functions
from django.contrib.auth.mixins import LoginRequiredMixin #  Login required for Class-based Views

from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt

# ---------------- Home ----------------------------


def home(request):
  return render(request, 'home.html')

def about(request):
  return render(request, 'about.html')

@login_required
def profile(request):
  # profile = Profile.objects.get(user=request.user)
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

#-------------Create Profile----------------

class ProfileCreate(CreateView):
  model = Profile
  template_name = 'user/create_profile.html'
  fields = ['age', 'gender', 'location', 'is_couch_potato', 'favorites', 'latitude', 'longitude', 'is_active']
  success_url = reverse_lazy('profile')  # Replace 'profile-detail' with your actual URL pattern

  def form_valid(self, form):
      print('form_valid being executed')
      form.instance.user = self.request.user
      print(form)
      return super().form_valid(form)


# -------------------- User Area -------------------------------

@login_required
def match(request):
  print(request.user.id)
  ip = requests.get('https://api.ipify.org?format=json')
  ip_data = json.loads(ip.text)
  res = requests.get('http://ip-api.com/json/'+ip_data["ip"]) #get a json
  location_data_one = res.text #convert JSON to python dictionary
  location_data = json.loads(location_data_one) #loading location data one
  if request.method == 'POST':
    latitude = request.POST.get('latitude')
    longitude = request.POST.get('longitude')
    profile = Profile.objects.get(user=request.user)
    profile.latitude = latitude
    profile.longitude = longitude
    profile.save()
    return HttpResponse(status=200)
  profile = Profile.objects.get(user=request.user)
  context = {'data': location_data, 'ip': ip_data, 'profile': profile }
  return render(request, 'user/match.html', context)
  
  

# @csrf_exempt
# @require_POST
# def update_profile(request, profile_id):
#     field_id = request.POST.get('field_id')
#     new_value = request.POST.get('new_value')

#     # Get the Profile instance based on the profile_id
#     try:
#         profile = Profile.objects.get(id=profile_id)
#     except Profile.DoesNotExist:
#         return JsonResponse({'error': 'Profile not found'}, status=404)

#     if field_id == 'location':
#         profile.location = new_value
#     elif field_id == 'favorites':
#         profile.favorites = new_value
#     else:
#         return JsonResponse({'error': 'Invalid field ID'}, status=400)

#     profile.save()

#     return JsonResponse({'message': 'Profile updated successfully'}, status=200)


class CommentListView(LoginRequiredMixin, ListView):
    model = Comment
    template_name = 'user/profile.html'
    context_object_name = 'comments'
    ordering = ['-date']
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
  # photo-file maps to the "name" attr on the <input>
  photo_file = request.FILES.get('photo_file', None)
  if photo_file:
    s3 = boto3.client('s3')
    # Need a unique "key" (filename)
    # It needs to keep the same file extension
    # of the file that was uploaded (.png, .jpeg, etc.)
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