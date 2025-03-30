from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .forms import BookForm, CollectionForm
from .models import Book
import logging

logger = logging.getLogger(__name__)

@login_required
def provide_book_view(request):
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            book = form.save(commit=False)
            book.user = request.user
            book.save()
            messages.success(request, "Book submitted successfully!")
            return redirect('provide_page')  # Ensure this URL name matches your URL config
        else:
            messages.error(request, "There was an error submitting your book.")
    else:
        form = BookForm()
    logger.debug("DEBUG: form fields = %s", list(form.fields.keys()))
    return render(request, 'accounts/provide.html', {'form': form})

@login_required
def borrow_books_view(request):
    books = Book.objects.all().order_by('-created_at')
    # Render the existing "borrow.html" in "accounts/templates/accounts/"
    return render(request, 'accounts/borrow.html', {'books': books})