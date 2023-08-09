from django.contrib import admin
from .models import User, Profile, Comment, Photo

admin.site.register(Profile)
admin.site.register(Photo)
admin.site.register(Comment)