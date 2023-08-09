from django.forms import ModelForm
from .models import Profile

class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['location', 'age', 'gender', 'is_couch_potato', 'favorites']