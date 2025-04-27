from django.urls import path, include
from . import views
from .views import review_borrower
from .views import (
    provide_book_view, 
    borrow_books_view, 
    create_collection_view, 
    list_collection_view, 
    collection_detail_view, 
    edit_collection_view, 
    delete_collection_view, 
    book_detail,
    request_borrow_book,
    list_borrow_request_view,
    list_my_borrow_request_view,
    handle_borrow_request_view,
    my_books_view,
    delete_book_view,
    list_my_collections_view,
)

urlpatterns = [
    path('provide/', provide_book_view, name='provide_page'),
    path('borrow/', borrow_books_view, name='borrow_page'),
    path('collection/create/', create_collection_view, name='create_collection_page'),
    path('collection/list/', list_collection_view, name='list_collection_page'),
    path('collection/<int:pk>/', collection_detail_view, name='collection_detail'),
    path('collection/<int:pk>/edit/', edit_collection_view, name='edit_collection'),
    path('detail/<int:book_id>/', book_detail, name='book_detail'),
    path('request_borrow/<int:book_id>/', request_borrow_book, name='request_borrow_book'),
    path('collection/<int:pk>/delete/', delete_collection_view, name='delete_collection'),
    path('borrow_request/list/', list_borrow_request_view, name='list_borrow_request_page'),
    path('borrow_request/my_list/', list_my_borrow_request_view, name='list_my_borrow_request_page'),
    path('borrow_request/<int:request_id>/<str:action>/', handle_borrow_request_view, name='handle_borrow_request'),
    path('review_borrower/<int:request_id>/', review_borrower, name='borrower_review'),
    path('my-books/', my_books_view, name='my_books'),
    path('delete-book/<int:book_id>/', delete_book_view, name='delete_book'),
    path('collections/my-collections/', list_my_collections_view, name='list_my_collections'),
]