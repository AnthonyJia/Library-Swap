from allauth.account.forms import SignupForm
from django import forms
from .models import CustomUser

class CustomSignupForm(SignupForm):
    USER_TYPE_CHOICES = CustomUser.USER_TYPE_CHOICES

    user_type = forms.ChoiceField(
        choices=USER_TYPE_CHOICES,
        widget=forms.RadioSelect,
        label="What is your role?"
    )

    def save(self, request):
        # Create the user via allauth’s default
        user = super().save(request)
        # Assign the chosen user_type
        user.user_type = self.cleaned_data['user_type']
        user.save()
        return user