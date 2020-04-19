from django.shortcuts import render, get_object_or_404
from django.utils.decorators import method_decorator
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, HttpResponseRedirect
from .forms import AdminLoginForm, AddBookForm
from django.contrib import messages
from .decorators import admin_required
from django.urls import reverse
from django.core.paginator import Paginator
from books.models import Book
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt



def admin_logout_view(request):
    logout(request)

    return redirect('admin:admin-login')


class AdminLoginView(View):
    template_name = 'admin_login.html'
    form_class = AdminLoginForm

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('admin:admin-book-list')

        return render(request, self.template_name)

    def post(self, request):
        login_form = self.form_class(request.POST)
        if login_form.is_valid():
            user = authenticate(
                username=login_form.cleaned_data['username'],
                password=login_form.cleaned_data['password']
            )

            if user is not None and user.is_superuser:
                login(request, user)
                return redirect('admin:admin-book-list')

            messages.error(request, 'Username or Password Invalid')

        return redirect(reverse('admin:admin-login'))


class DashboardView(View):
    template_name = 'admin_dashboard.html'

    @method_decorator(admin_required)
    def get(self, request):
        return render(request, self.template_name)


class ListBookView(View):
    template_name = 'admin_book_list.html'
    paginate = 10

    @method_decorator(admin_required)
    def get(self, request):

        books = Book.objects.order_by('-updated_at')
        paginator = Paginator(books, self.paginate)

        page = request.GET.get('page')
        books_object = paginator.get_page(page)
        context = {
            'books': books_object
        }
        return render(request, self.template_name, context)


class AddBookView(View):
    template_name = 'add_book.html'
    form_class = AddBookForm

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        return super().form_valid(form)

    @method_decorator(admin_required)
    def get(self, request):

        return render(request, self.template_name)

    @method_decorator(admin_required)
    def post(self, request):
        add_book_form = self.form_class(request.POST, request.FILES)
        if add_book_form.is_valid():
            add_book_form.save()

            return redirect('admin:admin-book-list')

        return render(request, self.template_name, {'form': add_book_form})


class DeleteBook(View):

    def dispatch(self, *args, **kwargs):
        method = self.request.POST.get('_method', '').lower()
        if method == 'put':
            return self.put(*args, **kwargs)
        if method == 'delete':
            return self.delete(*args, **kwargs)
        return super(DeleteBook, self).dispatch(*args, **kwargs)

    @method_decorator(admin_required)
    @csrf_exempt
    def delete(self, request, *args, **kwargs):
        book_id = kwargs.get('book_id')
        book = get_object_or_404(Book, pk=book_id)
        book.image.delete()
        book.delete()

        response = {
            'code': 'success'
        }

        return JsonResponse(response)


class EditBook(View):
    template_name = 'update_book.html'

    def dispatch(self, *args, **kwargs):
        method = self.request.POST.get('_method', '').lower()
        if method == 'put':
            return self.put(*args, **kwargs)
        if method == 'delete':
            return self.delete(*args, **kwargs)
        return super(EditBook, self).dispatch(*args, **kwargs)

    @method_decorator(admin_required)
    def get(self, request, *args, **kwargs):
        book_id = kwargs.get('book_id')
        book = get_object_or_404(Book, pk=book_id)
        form = AddBookForm(instance=book)
        context = {
            'book': book,
            'form': form
        }
        return render(request, self.template_name, context)

    @method_decorator(admin_required)
    @csrf_exempt
    def put(self, request, *args, **kwargs):
        book_id = request.POST['book_id']
        book = get_object_or_404(Book, pk=book_id)
        form = AddBookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            messages.success(request, 'Update Book Success !')

        return redirect(reverse('admin:admin-edit-book', kwargs={'book_id': book_id}))

