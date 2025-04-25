from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .forms import BookForm, CollectionForm, BorrowRequestForm, BorrowerReviewForm
from .models import Book, Collection, BorrowRequest, BorrowHistory, BorrowerReview
import logging
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.shortcuts import render
from django.db.models import Q
from books.models import Book

logger = logging.getLogger(__name__)

@login_required
def provide_book_view(request):
    if request.user.role != 'provider':
        messages.error(request, "Access Denied: You must be an approved provider to access this page.")
        return redirect('choose')
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
    query = request.GET.get('q', '').strip()
    private_collections = Collection.objects.filter(visibility='private')
    private_books = Book.objects.filter(collection__in=private_collections)
    books = Book.objects.exclude(id__in=private_books.values('id'))

    if query:
        books = books.filter(
            Q(title__icontains=query) |
            Q(author__icontains=query) |
            Q(genre__icontains=query)
        )
    
    books = books.order_by('-created_at')
    return render(request, 'accounts/borrow.html', {'books': books, 'query': query})

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
        old_visibility = collection.visibility  # Save original visibility
        form = CollectionForm(request.POST, instance=collection)

        if form.is_valid():
            updated_collection = form.save(commit=False)
            new_visibility = updated_collection.visibility
            updated_collection.save()
            form.save_m2m()

            # If visibility changed from public to private, or remains private, ensure creator is in allowed_users
            if new_visibility == 'private':
                updated_collection.allowed_users.add(updated_collection.creator)
                
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
def book_detail(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    return render(request, 'books/detail.html', {'book': book})

@login_required
def request_borrow_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)

    # Check if the book already has a current borrower
    if book.current_borrower:
        # If the book has a borrower, show a message and prevent form submission
        messages.error(request, f"The book '{book.title}' is already borrowed by someone else.")
        return redirect('book_detail', book_id=book.id)

    if request.method == 'POST':
        form = BorrowRequestForm(request.POST)
        if form.is_valid():
            borrow_request = form.save(commit=False)
            borrow_request.requester = request.user
            borrow_request.book = book 
            borrow_request.save()
            messages.success(request, "Borrow request has been submitted successfully!")
            return redirect('book_detail', book_id=book.id)
    else:
        form = BorrowRequestForm()

    return render(request, 'books/borrow_request_form.html', {
        'form': form,
        'book': book
    })

@login_required
def review_borrower(request, request_id):
    borrow_request = get_object_or_404(
        BorrowRequest,
        pk=request_id,
        status='returned',
        book__user=request.user
    )

    if hasattr(borrow_request, 'review'):
        return redirect('list_borrow_request_page')
    
    if request.method == 'POST':
        form = BorrowerReviewForm(request.POST)
        if form.is_valid():
            BorrowerReview.objects.create(
                borrow_request=borrow_request,
                reviewer=request.user,
                borrower=borrow_request.requester,
                rating=form.cleaned_data['rating']
            )
            messages.success(request, "Review submitted successfully!")
            return redirect('list_borrow_request_page')
    else:
        form = BorrowerReviewForm()
    
    return render(request, 'books/review_form.html', {'form': form, 'br': borrow_request})

@login_required
def list_my_borrow_request_view(request):
    borrow_requests = BorrowRequest.objects.filter(requester = request.user)
    return render(request, 'books/my_borrow_request_list.html', {'borrow_requests': borrow_requests})


@login_required
def list_borrow_request_view(request):
    borrow_requests = BorrowRequest.objects.all()
    return render(request, 'books/borrow_request_list.html', {'borrow_requests': borrow_requests})

@login_required
def handle_borrow_request_view(request, request_id, action):
    borrow_request = get_object_or_404(BorrowRequest, pk=request_id)

    if not request.user.role == 'provider':
        messages.error(request, "You don't have permission to perform this action.")
        return redirect('choose')  # Adjust this to wherever you want unauthorized users to go

    if action == 'accept':
        if borrow_request.book.current_borrower is None:
            borrow_request.status = 'approved'
            borrow_request.responded_by = request.user
            borrow_request.approved_at = timezone.now()
            borrow_request.book.current_borrower = borrow_request.requester
            borrow_request.book.save()
            messages.success(request, "Request accepted.")
        else:
            messages.error(request, "Book is currently being borrowed by someone else.")
            
    elif action == 'decline':
        borrow_request.status = 'rejected'
        borrow_request.responded_by = request.user
        borrow_request.approved_at = timezone.now()
        messages.success(request, "Request declined.")

    elif action == 'returned':
        if borrow_request.status != 'approved':
            messages.warning(request, "Only approved requests can be marked as returned.")
        else:
            borrow_request.status = 'returned'
            borrow_request.book.current_borrower = None
            borrow_request.book.save()
            borrow_request.save()
            messages.success(request, "Book marked as returned.")

            return redirect('borrower_review', request_id=borrow_request.id)

    else:
        messages.error(request, "Invalid action.")
        return redirect('choose') 

    borrow_request.save()
    return redirect('book_detail', book_id=borrow_request.book.id) 

@login_required
def my_books_view(request):
    if not request.user.is_provider_approved:
        messages.error(request, "Access Denied: You must be provider-approved to view your lending books.")
        return redirect('choose')

    books = Book.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'books/my_books.html', {'books': books})

@login_required
def delete_book_view(request, book_id):
    book = get_object_or_404(Book, id=book_id, user=request.user)
    
    if request.method == 'POST':
        book.delete()
        messages.success(request, "Book deleted successfully.")
        return redirect('my_books')

    return render(request, 'books/confirm_delete.html', {'book': book})
