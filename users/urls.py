from django.urls import path
from . import views as auth_views
from .views import RegisterView
from books import views as book_views

app_name = 'user'

urlpatterns = [
    path('', book_views.BookListView.as_view(), name='index'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('logout/', auth_views.logout_view, name='logout'),
]