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
    path('edit-book/<int:book_id>/', auth_views.EditBookView.as_view(), name='admin-edit-book'),
    path('list-user/', auth_views.ListUserView.as_view(), name='admin-list-user'),
    path('edit-user/<int:user_id>/', auth_views.EditUserView.as_view(), name='admin-edit-user'),
    path('delete-user/', auth_views.DeleteUserView.as_view(), name='admin-delete-user'),
    path('add-user/', auth_views.AddUserView.as_view(), name='admin-add-user'),
    path('request-book/', auth_views.RequestBookView.as_view(), name='admin-request-book'),
]