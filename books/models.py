from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User

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
    
    def is_available(self):
        return not self.borrow_requests.filter(status='approved').exists()
    
class Collection(models.Model):
    PRIVACY_CHOICES = [
        ('public', 'Public'),
        ('private', 'Private'),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    books = models.ManyToManyField(Book)
    visibility = models.CharField(
        max_length=7,  
        choices=PRIVACY_CHOICES,
        default='public',
    )
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE, 
        related_name='collections' 
    )
    allowed_users = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        blank=True,
        related_name='shared_collections',
        help_text="Only for private collections"
    )

    def __str__(self):
        return f"{self.title} ({self.visibility})"


class BorrowRequest(models.Model):
    REQUEST_STATUS = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('returned', 'Returned'),
    ]

    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='borrow_requests')
    requester = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='borrow_requests_list')
    message = models.TextField(blank=True)
    requested_at = models.DateTimeField(auto_now_add=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=10, choices=REQUEST_STATUS, default='pending')
    approved_at = models.DateTimeField(null=True, blank=True)
    responded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='handled_requests'
    )

    def __str__(self):
        return f"Request by {self.requester} for '{self.book.title}' ({self.status})"
