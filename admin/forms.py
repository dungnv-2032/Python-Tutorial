from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User
from books.models import Book
from django.forms import DateTimeField


class AdminLoginForm(forms.Form):
    username = forms.CharField(min_length=4, max_length=200)
    password = forms.CharField(min_length=6, max_length=200)


class AddBookForm(forms.ModelForm):
    #
    # def form_valid(self, form):
    #     # This method is called when valid form data has been POSTed.
    #     # It should return an HttpResponse.
    #     return super().form_valid(form)

    class Meta:
        model = Book
        fields = ['name', 'category', 'description', 'author', 'price', 'publish_date', 'number_page', 'image']


