from django import forms
from .models import Book, Collection

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        # Include all desired fields
        fields = ['title', 'author', 'genre', 'description', 'image']
        labels = {
            'description': 'Description (Optional)',
        }
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter book title'
            }),
            'author': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter author name'
            }),
            'genre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter genre'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Enter book description',
                'rows': 3
            }),
            'image': forms.ClearableFileInput(attrs={
                'class': 'form-control'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make these fields required
        self.fields['title'].required = True
        self.fields['author'].required = True
        self.fields['genre'].required = True
        self.fields['image'].required = True
        # Description remains optional
        self.fields['description'].required = False
class CollectionForm(forms.ModelForm):
     class Meta:
        model = Collection
        fields = ['title', 'description', 'books', 'visibility', 'allowed_users']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter title'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'books': forms.SelectMultiple(attrs={'class': 'form-control select2'}),
            'visibility': forms.Select(attrs={'class': 'form-control'}),
            'allowed_users': forms.SelectMultiple(attrs={'class': 'form-control select2'}),
        }

class CollectionForm(forms.ModelForm):
    class Meta:
        model = Collection
        fields = ['title', 'description', 'visibility', 'allowed_users', 'books']
        labels = {
            'title': 'Collection Title',
            'description': 'Description (Optional)',
            'visibility': 'Privacy',
            'allowed_users': 'Allowed Users',
            'books': 'Books in Collection',
        }
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter collection title'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter description (optional)', 'rows': 3}),
            'visibility': forms.Select(attrs={'class': 'form-control'}),
            'allowed_users': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'books': forms.SelectMultiple(attrs={'class': 'form-control'}),
        }