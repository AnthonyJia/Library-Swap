# projectb18/adapters.py

from django.contrib.auth import get_user_model
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter

User = get_user_model()

class MySocialAccountAdapter(DefaultSocialAccountAdapter):
    def pre_social_login(self, request, sociallogin):
        """
        Force AllAuth to auto-link the Google login to an existing user if
        the email already exists in the database, skipping any conflict form.
        """
        # If the user is already logged in, do nothing
        if request.user.is_authenticated:
            return

        # If Google provides an email
        email = sociallogin.user.email
        if email:
            try:
                # Look for a user with the same email
                existing_user = User.objects.get(email=email)
                # Link this social login to that existing user
                sociallogin.connect(request, existing_user)
            except User.DoesNotExist:
                # No existing user → AllAuth can auto-create one
                pass

    def is_auto_signup_allowed(self, request, sociallogin):
        # Always skip the sign-up form
        return True

    def requires_additional_signup(self, request, sociallogin):
        # Never show the final sign-up form
        return False