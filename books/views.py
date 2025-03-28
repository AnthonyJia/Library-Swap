from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import BookForm, CollectionForm
from .models import Book
import logging

@login_required
def provide_book_view(request):
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            book = form.save(commit=False)
            book.user = request.user
            book.save()
            messages.success(request, "Book submitted successfully!")
            return redirect('provide_page')  # or your proper URL name
        else:
            messages.error(request, "There was an error submitting your book.")
    else:
        form = BookForm()
    logger = logging.getLogger(__name__)
    logger.debug("DEBUG: form fields = %s", list(form.fields.keys()))
    return render(request, 'accounts/provide.html', {'form': form})

@login_required
def borrow_books_view(request):
    books = Book.objects.all().order_by('-created_at')
    # Render the existing "borrow.html" in "accounts/templates/accounts/"
    return render(request, 'accounts/borrow.html', {'books': books})

@login_required
def create_collection_view(request):
    if request.method == 'POST':
        form = CollectionForm(request.POST)
        if form.is_valid():
            collection = form.save(commit=False)
            collection.creator = request.user  # set the creator
            collection.save()  # Save early to get an ID, required for many-to-many access

            form.save_m2m()  # Save m2m relations now so we can access collection.books.all()

             # Now do the validation
            if not collection.books.exists():
                messages.error(request, "A collection must contain at least one book.")
                collection.delete()  # Optional cleanup
                return redirect('create_collection_page')

            for book in collection.books.all():
                other_collections = book.collection_set.exclude(id=collection.id)
                if collection.visibility == 'private':
                    if other_collections.exists():
                        messages.error(request, f"Book '{book.title}' cannot be added to a private collection if it already belongs to other collections.")
                        collection.delete()  # Optional cleanup
                        return redirect('create_collection_page')
                else:
                    private_collections = other_collections.filter(visibility='private')
                    if private_collections.exists():
                        messages.error(request, f"Book '{book.title}' is already in a private collection and cannot be added to a public collection.")
                        collection.delete()  # Optional cleanup
                        return redirect('create_collection_page')

            messages.success(request, "Collection created successfully!")
            return redirect('choose')  # Redirect to the target page
        else:
            print(form.errors)
            messages.error(request, "There was an error with your form.")
    else:
        form = CollectionForm()

    return render(request, 'books/create_collection.html', {'form': form})
