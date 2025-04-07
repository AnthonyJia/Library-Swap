from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('borrower', 'Borrower'),
        ('provider', 'Provider'),
    )

    # Choice field for user role
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, blank=True, null=True)

    # Field to store admin approval for providers
    is_provider_approved = models.BooleanField(default=False)

    # New field for storing the user’s profile picture
    # Images will be uploaded to S3 in the 'profile_pics/' folder.
    image = models.ImageField(upload_to='profile_pics/', blank=True, null=True)

    # Additional fields
    birthday = models.DateField(blank=True, null=True)
    interests = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    def save(self, *args, **kwargs):
        """
        Overridden save method:
        - If the user is approved but not currently a provider, set them to 'provider'.
        """
        if self.is_provider_approved and self.role != 'provider':
            self.role = 'provider'
        super().save(*args, **kwargs)

    def __str__(self):
        return self.username