from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.views import View
from django.shortcuts import redirect, HttpResponseRedirect, HttpResponse
from .models import Book, Book_History, Book_Request, Book_Comment
from .forms import BookSearchForm, AddBookForm, AddBookComment
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


class BookListView(LoginRequiredMixin, View):
    template_name = 'index.html'

    def get(self, request):
        books = Book.objects.order_by('-updated_at')
        context = {
            'books': books,
        }
        return render(request, self.template_name, context)


def get_book_detail(request, *args, **kwargs):

    book_id = kwargs.get('book_id')
    user = request.user
    book = get_object_or_404(Book, pk=book_id)

    book_history, created = Book_History.objects.get_or_create(
        book=book,
        user=user,
    )

    context = {
        'book': book,
        'book_history': book_history,
        'follow_status': book_history.get_follow_status(),
        'like_status': book_history.get_like_status(),
    }
    return context


class BookDetailView(LoginRequiredMixin, View):
    template_name = 'book_detail.html'

    def get(self, request, *args, **kwargs):
        context = get_book_detail(request, *args, **kwargs)

        return render(request, self.template_name, context)


class BookSearchView(LoginRequiredMixin, View):
    template_name = 'index.html'
    form_class = BookSearchForm

    def get(self, request, *args, **kwargs):
        book_search_form = self.form_class(request.GET)
        if book_search_form.is_valid():
            text = book_search_form.cleaned_data['text']
            books = Book.objects.filter(name__contains=text)
            context = {
                'books': books,
                'text': text,
            }
            return render(request, self.template_name, context)

        return render(request, self.template_name, {'errors': book_search_form.errors})


class BookCategoryView(LoginRequiredMixin, View):
    template_name = 'index.html'

    def get(self, request, *args, **kwargs):
        category_id = kwargs.get('id')
        books = Book.objects.filter(category_id=category_id)
        context = {
            'books': books,
        }

        return render(request, self.template_name, context)


class BookHistoryView(LoginRequiredMixin, View):
    template_name = 'index.html'

    def get(self, request):
        user = request.user
        books = Book.objects.filter(book_history__user=user).order_by('-updated_at')
        context = {
            'books': books,
        }

        return render(request, self.template_name, context)


class BookFollowView(LoginRequiredMixin, View):

    @csrf_exempt
    def post(self, request, *args, **kwargs):

        book_id = request.POST['book_id']
        user = request.user
        book_history, created = Book_History.objects.get_or_create(
            book_id=book_id,
            user=user,
        )

        unfollow_status = Book.UNFOLLOW
        follow_status = book_history.follow_status
        if follow_status == unfollow_status:
            follow_status = Book.FOLLOW;
        else:
            follow_status = unfollow_status
        book_history.follow_status = follow_status
        book_history.save()

        index_status = Book.UNFOLLOW
        if index_status == follow_status:
            index_status = Book.FOLLOW
        response = {
            'code': 'success',
            'follow_status': Book.FOLLOW_STATUS[index_status]
        }
        return JsonResponse(response)


class BookLikeView(LoginRequiredMixin, View):

    @csrf_exempt
    def post(self, request, *args, **kwargs):

        book_id = request.POST['book_id']
        user = request.user
        book_history, created = Book_History.objects.get_or_create(
            book_id=int(book_id),
            user=user,
        )

        unlike_status = Book.UNLIKE
        like_status = book_history.like_status
        if like_status == unlike_status:
            like_status = Book.LIKE;
        else:
            like_status = unlike_status
        book_history.like_status = like_status
        book_history.save()

        index_status = Book.UNLIKE
        if index_status == like_status:
            index_status = Book.LIKE

        response = {
            'code': 'success',
            'like_status': Book.LIKE_STATUS[index_status]
        }
        return JsonResponse(response)


class BookReadView(LoginRequiredMixin, View):

    @csrf_exempt
    def post(self, request, *args, **kwargs):
        book_id = request.POST['book_id']
        read_status = request.POST['read_status']
        user = request.user

        book_history, created = Book_History.objects.get_or_create(
            book_id=int(book_id),
            user=user,
        )

        book_history.read_status = read_status
        book_history.save()

        response = {
            'code': 'success',
            'read_status': Book.READING,
        }
        return JsonResponse(response)


class BookFavoriteView(LoginRequiredMixin, View):
    template_name = 'index.html'

    def get(self, request):
        user = request.user
        books = Book.objects.filter(book_history__user=user, book_history__follow_status=True).order_by('-updated_at')
        context = {
            'books': books,
        }

        return render(request, self.template_name, context)


class BookRateView(LoginRequiredMixin, View):

    @csrf_exempt
    def post(self, request, *args, **kwargs):
        book_id = request.POST['book_id']
        rate = request.POST['rate']
        user = request.user

        book_history, created = Book_History.objects.get_or_create(
            book_id=int(book_id),
            user=user,
        )

        book_history.rate = rate
        book_history.save()

        response = {
            'code': 'success',
        }
        return JsonResponse(response)


class BookRequestListView(LoginRequiredMixin, View):
    template_name = 'book_request_list.html'

    def get(self, request):
        user = request.user
        book_request = Book_Request.objects.filter(user=user).order_by('-updated_at')

        context = {
            'book_requests': book_request
        }
        return render(request, self.template_name, context)


class AddBookRequest(LoginRequiredMixin, View):
    template_name = 'add_book_request.html'
    form_class = AddBookForm

    def get(self, request):

        return render(request, self.template_name)

    @csrf_exempt
    def post(self, request, *args, **kwargs):

        add_book_form = self.form_class(request.POST)
        if add_book_form.is_valid():
            user = request.user
            Book_Request.objects.create(
                name=request.POST['name'],
                price=request.POST['price'],
                note=request.POST['note'],
                user=user,
                category_id=request.POST['category_id']
            )

            return redirect('book:book-request-list')
        return render(request, self.template_name, {'add_book_form': add_book_form})


class AddBookComment(LoginRequiredMixin, View):
    form_class = AddBookComment
    template_name = 'book_detail.html'

    @csrf_exempt
    def post(self, request, *args, **kwargs):
        kwargs['book_id'] = request.POST['book_id']

        add_comment_form = self.form_class(request.POST)
        if add_comment_form.is_valid():
            user = request.user

            Book_Comment.objects.create(
                user=user,
                comment=request.POST['comment'],
                book_id=request.POST['book_id']
            )

        return redirect(reverse('book:book-detail', kwargs={'book_id': request.POST['book_id']}))
