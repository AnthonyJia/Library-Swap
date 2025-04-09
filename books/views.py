from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .forms import BookForm, CollectionForm
from .models import Book, Collection
import logging
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone

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

def borrow_books_view(request):
    # Fetch all private collections
    private_collections = Collection.objects.filter(visibility = 'private')

    # Get the books that belong to private collections (via ManyToMany field)
    private_books = Book.objects.filter(collection__in=private_collections)

     # Fetch all books excluding those that are in private collections
    public_books = Book.objects.exclude(id__in=private_books.values('id')).order_by('-created_at')

    # Render the existing "borrow.html" in "accounts/templates/accounts/"
    return render(request, 'accounts/borrow.html', {'books': public_books})

@login_required
def create_collection_view(request):
    if request.method == 'POST':
        form = CollectionForm(request.POST)
        if form.is_valid():
            collection = form.save(commit=False)
            collection.creator = request.user  # set the creator
            collection.save()  # Save early to get an ID
            form.save_m2m()  # Save many-to-many relationships

            # Automatically grant the creator access to private collections.
            if collection.visibility == 'private':
                collection.allowed_users.add(request.user)

            # Validation: Check that at least one book is added
            if not collection.books.exists():
                messages.error(request, "A collection must contain at least one book.")
                collection.delete() 
                return redirect('create_collection_page')
            
            # Validation: Only provider-approved users can create private collections.
            if collection.visibility == 'private' and not request.user.is_provider_approved:
                messages.error(request, "You must be provider approved to create a private collection.")
                collection.delete()
                return redirect('create_collection_page')
            
            # Validation: If the user is a borrower, they cannot create private collections.
            if request.user.role == 'borrower' and collection.visibility == 'private':
                messages.error(request, "Patrons cannot create private collections.")
                collection.delete()
                return redirect('create_collection_page')

            # Validate each book's collection constraints
            for book in collection.books.all():
                other_collections = book.collection_set.exclude(id=collection.id)
                if collection.visibility == 'private':
                    if other_collections.exists():
                        messages.error(request, f"Book '{book.title}' cannot be added to a private collection if it already belongs to other collections.")
                        collection.delete()
                        return redirect('create_collection_page')
                else:
                    private_collections = other_collections.filter(visibility='private')
                    if private_collections.exists():
                        messages.error(request, f"Book '{book.title}' is already in a private collection and cannot be added to a public collection.")
                        collection.delete()
                        return redirect('create_collection_page')

            messages.success(request, "Collection created successfully!")
            return redirect('choose')  # Redirect to the target page
        else:
            print(form.errors)
            messages.error(request, "There was an error with your form.")
    else:
        form = CollectionForm()

    return render(request, 'books/create_collection.html', {'form': form})

def list_collection_view(request):
    collections = Collection.objects.all()  # Query all collections
    return render(request, 'books/collection_list.html', {'collections': collections})

@login_required
def collection_detail_view(request, pk):
    collection = get_object_or_404(Collection, pk=pk)
    books_in_collection = Book.objects.filter(collection=collection)

    if collection.visibility == 'public':
        return render(request, 'books/collection_detail.html', {
            'collection': collection,
            'books': books_in_collection,
        })
    
    # If it's private, only allow users in the allowed_users set.
    elif collection.visibility == 'private':
        if request.user in collection.allowed_users.all():
            return render(request, 'books/collection_detail.html', {
                'collection': collection,
                'books': books_in_collection,
            })
        else:
            messages.error(request, "You do not have access to this private collection.")
            return redirect('list_collection_page')
    else:
        return render(request, 'books/collection_detail.html', {
            'collection': collection,
            'books': books_in_collection,
        })

@login_required
def edit_collection_view(request, pk):
    collection = get_object_or_404(Collection, pk=pk)
    # Only the creator can edit the collection.
    if collection.creator != request.user:
        messages.error(request, "You do not have permission to edit this collection.")
        return redirect('books/collection_detail', pk=collection.pk)
    
    if request.method == 'POST':
        form = CollectionForm(request.POST, instance=collection)
        if form.is_valid():
            form.save()
            messages.success(request, "Collection updated successfully!")
            return redirect('collection_detail', pk=collection.pk)
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = CollectionForm(instance=collection)
    
    return render(request, 'books/edit_collection.html', {'form': form, 'collection': collection})

@login_required
def delete_collection_view(request, pk):
    collection = get_object_or_404(Collection, pk=pk)
    # Only the creator can delete the collection.
    if collection.creator != request.user:
        messages.error(request, "You do not have permission to delete this collection.")
        return redirect('books/collection_detail', pk=collection.pk)
    
    if request.method == 'POST':
        collection.delete()
        messages.success(request, "Collection deleted successfully!")
        return redirect('list_collection_page')  # Or another page, such as a collection list view.
    
    return render(request, 'books/delete_collection.html', {'collection': collection})

@login_required
def borrow_book(request, book_id):
    book = get_object_or_404(Book, pk=book_id)

    if book.is_available():
        book.borrowed_by = request.user
        book.borrowed_at = timezone.now()
        book.save()
    # else: maybe show a message "Already borrowed."

    return redirect('book_detail', book_id=book.id) 

@login_required
def book_detail(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    return render(request, 'books/detail.html', {'book': book})
