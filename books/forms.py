from django import forms
from .models import Book, Collection

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'description', 'image']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter book title'
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