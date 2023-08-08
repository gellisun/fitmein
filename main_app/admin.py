from django.contrib import admin
from .models import CustomUser
from django.contrib.auth.admin import UserAdmin


class CustomUserAdmin(UserAdmin):
    list_display = ['username', 'email', 'age', 'gender', 'city']

admin.site.register(CustomUser, CustomUserAdmin)
# admin.site.register(Badges)
# Register your models here.
