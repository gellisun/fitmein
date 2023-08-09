from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('accounts/signup/', views.signup, name='signup'),
    path('profile/create/', views.ProfileCreate.as_view(), name='create_profile'),
    path('profile/', views.profile, name='profile'),
    path('match/', views.match, name='match'),
    path('match/update_activity/<int:pk>/', views.ActivityUpdate.as_view(), name='update_activity'),
    path('table/', views.find_match, name='find_match'),
    path('create/', views.CommentCreateView.as_view(), name='create_comment'),
    path('edit/<int:pk>/', views.CommentUpdateView.as_view(), name='edit_comment'),
    path('delete/<int:pk>/', views.CommentDeleteView.as_view(), name='delete_comment'),
    path('profile/<int:user_id>/', views.profile, name='profile'),
    path('add_photo/<int:user_id>/', views.add_photo, name='plant'),
    
]

