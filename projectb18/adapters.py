from allauth.socialaccount.adapter import DefaultSocialAccountAdapter

class MySocialAccountAdapter(DefaultSocialAccountAdapter):
    def is_auto_signup_allowed(self, request, sociallogin):
        """
        Return True to skip the 'Sign Up' form entirely.
        """
        return True

    def requires_additional_signup(self, request, sociallogin):
        """
        If this returns True, Allauth will show the sign-up form.
        We want to skip it, so return False.
        """
        return False