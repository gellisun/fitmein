from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('accounts/signup/', views.signup, name='signup'),
    path('profile/create/', views.ProfileCreate.as_view(), name='create_profile'),
    path('profile/', views.profile, name='profile'),
    path('profile/<int:user_id>/', views.view_friend_profile, name='view_friend_profile'),
    path('match/', views.match, name='match'),
    path('match/update_activity/<int:pk>/', views.ActivityUpdate.as_view(), name='update_activity'),
    path('my_match/<str:latitude>/<str:longitude>/', views.my_match, name='my_match'),
    path('find/<int:profile_id>/', views.find_match, name='find_match'),
    path('create/', views.CommentCreateView.as_view(), name='create_comment'),
    path('edit/<int:pk>/', views.CommentUpdateView.as_view(), name='edit_comment'),
    path('delete/<int:pk>/', views.CommentDeleteView.as_view(), name='delete_comment'),
    path('add_photo/<int:user_id>/', views.add_photo, name='plant'),
    path('profile/update_profile/<int:pk>/', views.ProfileUpdate.as_view(), name='update_profile')  
    
]

