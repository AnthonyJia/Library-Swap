from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .forms import UserImageForm
from books.forms import BookForm
from books.models import Book, Collection

def home(request):
    return render(request, 'accounts/home.html')

def anonymous_view(request):
    return render(request, 'accounts/anonymous.html')

@login_required
def choose_view(request):
    if request.method == 'POST':
        choice = request.POST.get('choice')  # 'provider' or 'borrower'
        
        if choice == 'provider':
            # Check if the user is approved
            if request.user.is_provider_approved:
                request.user.role = 'provider'
                request.user.save()
                return redirect('provide_page')
            else:
                messages.error(request, "You do not have permission to be a provider yet.")
                return redirect('choose')
        elif choice == 'borrower':
            # They want to be a borrower
            request.user.role = 'borrower'
            request.user.save()
            return redirect('borrow_page')

    return render(request, 'accounts/choose.html')

@login_required
def provide_view(request):
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            book = form.save(commit=False)
            book.user = request.user  # Associate the book with the logged-in user
            book.save()
            messages.success(request, "Book submitted successfully!")
            return redirect('provide_page')  # Ensure this URL name matches your URL config
        else:
            messages.error(request, "There was an error submitting your book.")
    else:
        form = BookForm()
    return render(request, 'accounts/provide.html', {'form': form})

@login_required
def borrow_view(request):
    # Fetch all private collections
    private_collections = Collection.objects.filter(visibility = 'private')

    # Get the books that belong to private collections (via ManyToMany field)
    private_books = Book.objects.filter(collection__in=private_collections)

     # Fetch all books excluding those that are in private collections
    public_books = Book.objects.exclude(id__in=private_books.values('id')).order_by('-created_at')
    
    return render(request, 'accounts/borrow.html', {'books' : public_books})

@login_required
def profile_view(request):
    """
    Displays the user’s current profile (including profile picture).
    """
    return render(request, 'accounts/profile.html')

@login_required
def upload_picture_view(request):
    """
    Displays and processes the form for uploading/updating the profile picture.
    """
    if request.method == 'POST':
        form = UserImageForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile picture updated successfully!")
            return redirect('profile')  # Redirect back to profile page
        else:
            messages.error(request, "Error uploading your profile picture.")
    else:
        form = UserImageForm(instance=request.user)

    return render(request, 'accounts/upload_picture.html', {'form': form})