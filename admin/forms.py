from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User
from books.models import Book
from django.forms import DateTimeField


class AdminLoginForm(forms.Form):
    username = forms.CharField(min_length=4, max_length=200)
    password = forms.CharField(min_length=6, max_length=200)


class AddBookForm(forms.ModelForm):

    class Meta:
        model = Book
        fields = ['name', 'category', 'description', 'author', 'price', 'publish_date', 'number_page', 'image']


class AddUserForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class UpdateUserForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['username', 'email', 'password1', 'password2']

