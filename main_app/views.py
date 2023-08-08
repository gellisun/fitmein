from django.shortcuts import render, redirect
import requests
import json
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.urls import reverse_lazy

from .models import Profile, Badges, User, Comment
from .forms import ProfileForm, CommentForm

from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required #  Login required for View Functions
from django.contrib.auth.mixins import LoginRequiredMixin #  Login required for Class-based Views

from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt

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
            profile_form.instance.user = request.user 
            profile_form.save()
            return redirect('profile') 

 else:
    profile_form = ProfileForm(instance=profile)
    comments = Comment.objects.filter(user=profile.user)
    if profile_exists:
      profile_form = ProfileForm(instance=profile)
    else:
      profile_form = ProfileForm()
 context = {'profile': profile, 'profile_form': profile_form, 'comments': comments}
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

def match(request):
  ip = requests.get('https://api.ipify.org?format=json')
  ip_data = json.loads(ip.text)
  res = requests.get('http://ip-api.com/json/'+ip_data["ip"]) #get a json
  location_data_one = res.text #convert JSON to python dictionary
  location_data = json.loads(location_data_one) #loading location data one
  return render(request, 'user/match.html', {'data': location_data, 'ip': ip_data })

@csrf_exempt
@require_POST
def update_profile(request, profile_id):
    field_id = request.POST.get('field_id')
    new_value = request.POST.get('new_value')

    # Get the Profile instance based on the profile_id
    try:
        profile = Profile.objects.get(id=profile_id)
    except Profile.DoesNotExist:
        return JsonResponse({'error': 'Profile not found'}, status=404)

    if field_id == 'location':
        profile.location = new_value
    elif field_id == 'favorites':
        profile.favorites = new_value
    else:
        return JsonResponse({'error': 'Invalid field ID'}, status=400)

    profile.save()

    return JsonResponse({'message': 'Profile updated successfully'}, status=200)


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