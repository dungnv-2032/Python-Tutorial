from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User


class BookSearchForm(forms.Form):
    text = forms.CharField(min_length=1, max_length=200)


class AddBookForm(forms.Form):
    name = forms.CharField(min_length=1, max_length=500)
    price = forms.IntegerField(min_value=1)
    category_id = forms.IntegerField(max_value=5, min_value=1)
    note = forms.Textarea()


class AddBookComment(forms.Form):
    comment = forms.Textarea()
    book_id = forms.IntegerField(min_value=1)