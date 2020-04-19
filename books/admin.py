from django.contrib import admin
from .models import Book, Book_Comment, Book_History, Book_Request, Category
# Register your models here.


class AuthorAdmin(admin.ModelAdmin):
    pass


admin.site.register(Book, AuthorAdmin)
admin.site.register(Category, AuthorAdmin)
admin.site.register(Book_Request, AuthorAdmin)
admin.site.register(Book_Comment, AuthorAdmin)