from django.test import TestCase

# Create your tests here.

from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from .models import Book

User = get_user_model()

class BookModelTest(TestCase):
    def setUp(self):
        # Creates a user for testing
        self.user = User.objects.create_user(
            username='testuser', email='testuser@example.com', password='testpass'
        )

    def test_book_creation_without_uploader_email(self):
        """Ensure that if we create a Book with a user but no uploader_email,
        the uploader_email auto-fills with the user’s email."""
        book = Book.objects.create(
            user=self.user,
            title="Test Book",
            author="Test Author",
            genre="Fiction",
            description="A test book for unit testing",
        )
        self.assertEqual(book.uploader_email, "testuser@example.com")
        self.assertEqual(str(book), "Test Book")  # tests the __str__ method

    def test_book_creation_with_uploader_email(self):
        """If we explicitly set an uploader_email, it remains as is, even if user is set."""
        book = Book.objects.create(
            user=self.user,
            uploader_email='custom@example.com',
            title="Custom Email Book"
        )
        self.assertEqual(book.uploader_email, 'custom@example.com')

    def test_image_field(self):
        """Test that an image can be associated with the Book."""
        # Create a fake image
        fake_image = SimpleUploadedFile(
            "test_cover.jpg", b"fake-image-bytes", content_type="image/jpeg"
        )
        book = Book.objects.create(
            user=self.user,
            title="Image Test Book",
            image=fake_image
        )
        self.assertTrue(book.image.name.endswith("test_cover.jpg"))

    def test_auto_set_uploader_email_only_if_blank(self):
        """Check that uploader_email is set only if blank. 
           If we reassign, the user’s email shouldn’t overwrite it."""
        book = Book.objects.create(
            user=self.user,
            uploader_email='alreadyset@example.com',
            title="Already Set Email"
        )
        # Because the email was already set, it should remain
        self.assertEqual(book.uploader_email, 'alreadyset@example.com')

    def test_book_author_genre_defaults(self):
        """Ensure that author and genre can be blank and handle gracefully."""
        book = Book.objects.create(
            user=self.user,
            title="No Author/Genre"
        )
        self.assertEqual(book.author, "")
        self.assertEqual(book.genre, "")

