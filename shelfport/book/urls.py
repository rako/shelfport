from django.urls import path

from . import views

app_name = 'book'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('book-list/', views.BookListView.as_view(), name='book_list'),
    path('book-detail/<int:pk>/', views.BookDetailView.as_view(), name='book_detail'),
    path('book-create/', views.BookCreateView.as_view(), name='book_create'),
    path('book-update/<int:pk>/', views.BookUpdateView.as_view(), name='book_update'),
    path('book-delete/<int:pk>/', views.BookDeleteView.as_view(), name='book_delete'),
]