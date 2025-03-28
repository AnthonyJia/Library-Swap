from django import forms
from .models import Book

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