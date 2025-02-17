# myapp/adapters.py

from allauth.socialaccount.adapter import DefaultSocialAccountAdapter

class MySocialAccountAdapter(DefaultSocialAccountAdapter):
    def is_auto_signup_allowed(self, request, sociallogin):
        """
        Return True to always skip the 'Sign Up' form and go straight to login.
        """
        return True