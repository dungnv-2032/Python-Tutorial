from django.urls import path
from . import views as auth_views

app_name = 'admin'

urlpatterns = [
    path('', auth_views.DashboardView.as_view(), name='admin-dashboard'),
    path('login/', auth_views.AdminLoginView.as_view(), name='admin-login'),
    path('logout/', auth_views.admin_logout_view, name='admin-logout'),
    path('list-book/', auth_views.ListBookView.as_view(), name='admin-book-list'),
    path('add-book/', auth_views.AddBookView.as_view(), name='admin-add-book'),
    path('delete-book/', auth_views.DeleteBook.as_view(), name='admin-delete-book'),
    path('edit-book/<int:book_id>/', auth_views.EditBook.as_view(), name='admin-edit-book')

]