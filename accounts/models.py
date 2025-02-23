from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('borrower', 'Borrower'),
        ('provider', 'Provider'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, blank=True, null=True)
    def save(self, *args, **kwargs):
        # If the user is approved but not currently a provider, set them to provider
        if self.is_provider_approved and self.role != 'provider':
            self.role = 'provider'
        super().save(*args, **kwargs)

    # New field to store admin approval for providers
    is_provider_approved = models.BooleanField(default=False)

    def __str__(self):
        return self.username