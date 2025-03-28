from django.db import models
from django.conf import settings

class Book(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='books'
    )
    uploader_email = models.EmailField(blank=True)  # New field to store the uploader's email
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255, blank=True)
    genre = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='book_covers/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # Automatically set uploader_email if not already set and user exists.
        if self.user and not self.uploader_email:
            self.uploader_email = self.user.email
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title