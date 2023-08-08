from django.db import models
from django.core.validators import MinValueValidator
from django.urls import reverse
from django.contrib.auth.models import AbstractUser, UserManager
import datetime
from django.utils import timezone

GENDER = (('M', 'Male'),('F', 'Female'),('O', 'Other'))

ACTIVITIES = (('RU','Running'),('WL', 'Weight Lifting'),('GC','Group Classes'),('BR', 'Bike Riding'),('TE','Tennis'),('SQ','Squash'),('WA','Walking'),('BA','Badminton'),('SW','Swimming'),('WA','Walking'),('HI','Hiking'), ('P', 'Pilates'), ('SU', 'Surfing'), ('SK', 'Skateboarding'))

def get_profile_image_filepath(self, filename):
    return f'profile_images/{self.pk}/{"profile_image.png"}'

def get_profile_image_filename(self):
    return str(self.profile_image)[str(self.profile_image).index(f'profile_images/{self.pk}/'):]

# ------------------ Custom User Models ------------------------------

class CustomUserManager(UserManager):
    pass

class CustomUser(AbstractUser):
    gender = models.CharField(max_length=1, choices=GENDER)
    age = models.IntegerField(validators=[MinValueValidator(0)], default=0)  
    location = models.CharField(max_length=50)
    is_couch_potato = models.BooleanField(default=True)
    favorites = models.CharField(max_length=2, choices=ACTIVITIES)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    objects = CustomUserManager()

    def __str__(self):
        return self.username

    def get_absolute_url(self):
        return reverse('detail', kwargs={'user_id': self.id})


# ------------------------ END ------------------------------------

class UserProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.name + "'s Profile"    

# class Badges(models.Model):
#     name = models.CharField()
#     icon = models.ImageField(max_length=255, upload_to=get_profile_image_filepath)
#     profile = models.ManyToManyField(Profile)

class Matcher(models.Model):
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    chosen_activities = models.CharField(max_length=2, choices=ACTIVITIES)

    def __str__(self):
        return self.name
    
    