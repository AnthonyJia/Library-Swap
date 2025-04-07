# accounts/forms.py
from django import forms
from .models import CustomUser

class UserImageForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['image']

# For updating the user’s profile fields
class ProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = [
            'first_name',
            'last_name',
            'email',
            'birthday',
            'interests',
            'description',
        ]