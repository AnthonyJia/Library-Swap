from django.urls import path
from .views import provide_book_view, borrow_books_view, create_collection_view, list_collection_view

urlpatterns = [
    path('provide/', provide_book_view, name='provide_page'),
    path('borrow/', borrow_books_view, name='borrow_page'),
    path('collection/create/', create_collection_view, name='create_collection_page'),
    path('collection/list/', list_collection_view, name='list_collection_page' )
]