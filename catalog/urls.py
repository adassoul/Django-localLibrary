from django.urls import path
from . import views

'''
from .views import send_email
'''
urlpatterns = [
    path('', views.index, name='index'),
    path('books/', views.BookListView.as_view(), name='books'),
    path('book/<int:pk>', views.BookDetailView.as_view(), name='book-detail'),
    path('authors/', views.AuthorListView.as_view(), name='authors'),
    path('author/<pk>', views.AuthorDetailView.as_view(), name='author-detail')
]
'''
urlpatterns += [
    path('accounts/password_reset/done/', send_email),
]'''
# repath(r'^book/(?P<date>\d+)$',views.BookDetailView.as_view(), name='book-detail')
# date will be like 01012021 or 31121880 date[0:2]="01"(or "31") date[2:4]="01"(or 12) date[4:8]="2021"(or "1880")
urlpatterns += [
    path('mybooks/', views.LoanedBooksByUserListView.as_view(), name='my-borrowed'),
]

#challenge, part8
urlpatterns += [
    path('all-books/', views.AllBooksShownToLibrarianListView.as_view(), name='all-borrowed'),
]