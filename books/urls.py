from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views as auth_views
from django.contrib.staticfiles.urls import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from .views import (
    BookListView,
    BookDetailView,
    BookSearchView,
    BookCategoryView,
    BookHistoryView,
    BookFollowView,
    BookLikeView,
    BookReadView,
    BookFavoriteView,
    BookRateView,
    BookRequestListView,
    AddBookRequest,
    AddBookComment
)

app_name = 'book'

urlpatterns = [
    path('', BookListView.as_view(), name='index'),
    path('book-detail/<int:book_id>/', BookDetailView.as_view(), name='book-detail'),
    path('book-category/<int:id>/', BookCategoryView.as_view(), name='book-category-search'),
    path('book-search/', BookSearchView.as_view(), name='book-search'),
    path('book-history/', BookHistoryView.as_view(), name='book-history'),
    path('book-follow/', BookFollowView.as_view(), name='book-follow'),
    path('book-like/', BookLikeView.as_view(), name='book-like'),
    path('book-read/', BookReadView.as_view(), name='book-read'),
    path('book-favorite/', BookFavoriteView.as_view(), name='book-favorite'),
    path('book-rate/', BookRateView.as_view(), name='book-rate'),
    path('book-request-list/', BookRequestListView.as_view(), name='book-request-list'),
    path('add-book-request/', AddBookRequest.as_view(), name='add-book-request'),
    path('add-book-comment/', AddBookComment.as_view(), name='add-book-comment'),

]
