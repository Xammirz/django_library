
from django.urls import path, include
from django.urls.conf import include
from . import views
from .views import  BookListViewAPI, BookDetailViewAPI, AuthorListViewAPI, AuthorDetailViewAPI

from django.urls import path
from . import views

from django.conf.urls import url

urlpatterns = [

    path('', views.index, name='home'),
    path('books/', views.BookListView.as_view(), name='bookss'),
    url(r'^book/(?P<pk>\d+)$', views.BookDetailView.as_view(), name='book-detail'),
    path('authors/', views.AuthorListView.as_view(), name='authors'),
    url(r'^author/(?P<pk>\d+)$', views.AuthorDetailView.as_view(), name='author-detail'),
    path('mybooks/', views.LoanedBooksByUserListView.as_view(), name='my-borrowed'),
    path('book/<uuid:pk>/renew/', views.renew_book_librarian, name='renew-book-librarian'),
    path('arend/', views.ArendView.as_view(), name='arend'),
    path('adminactionauthor/', views.AdminActionAuthorView.as_view(), name='admin_action_author'),
    path('author/create/', views.AuthorCreate.as_view(), name='author-create'),
    path('author/update/<int:pk>', views.AuthorUpdate.as_view(), name='author-update'),
    path('author/delete/<int:pk>', views.AuthorDelete.as_view(), name='author-delete'),
    path('adminactionbook/', views.AdminActionBookView.as_view(), name='admin_action_book'),
    path('book/create/', views.BookCreate.as_view(), name='book-create'),
    path('book/update/<int:pk>', views.BookUpdate.as_view(), name='book-update'),
    path('book/delete/<int:pk>', views.BookDelete.as_view(), name='book-delete'),

    path('api/v1/books/', BookListViewAPI.as_view(), name='book_list_api'),
    path('api/v1/books/<int:pk>', BookDetailViewAPI.as_view(), name='book_detail_api'),
    path('api/v1/authors/', AuthorListViewAPI.as_view(), name='author_list_api'),
    path('api/v1/authors/<int:pk>', AuthorDetailViewAPI.as_view(), name='author_detail_api'),
    

]