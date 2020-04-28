from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User
from django.db.models import Avg


class Category(models.Model):
    name = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class BookBase(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Book(BookBase):

    UNFOLLOW = 0
    FOLLOW = 1
    FOLLOW_STATUS = (
        'Unfollow',
        'Follow'
    )

    UNLIKE = 0
    LIKE = 1
    LIKE_STATUS = (
        'Unlike',
        'Like'
    )

    UNREAD = 0
    READING = 1
    READ = 2
    READ_STATUS = (
        (UNREAD, 'Unread'),
        (READING, 'Reading'),
        (READ, 'Read'),
    )

    UNRATE = 0
    BAD = 1
    NORMAL = 2
    GOOD = 3
    VERY_GOOD = 4
    SUPER_GOOD = 5
    RATE = (
        (UNRATE, 'Unrate'),
        (BAD, 'Bad'),
        (NORMAL, 'Normal'),
        (GOOD, 'Good'),
        (VERY_GOOD, 'Very Good'),
        (SUPER_GOOD, 'Super Good')
    )

    name = models.CharField(max_length=500)
    description = models.TextField(null=True)
    author = models.CharField(max_length=200)
    price = models.IntegerField(default=0)
    category = models.ForeignKey(Category, on_delete=models.SET(0))
    publish_date = models.DateField()
    image = models.ImageField(verbose_name='image', upload_to='images/')
    number_page = models.IntegerField()

    def __str__(self):
        return self.name

    def count_follow(self):
        return Book_History.objects.filter(
            book=self,
            follow_status=Book_History.FOLLOW
        ).count()

    def get_avg_rate(self):
        avg_rate = Book_History.objects.filter(
            book=self,
        ).aggregate(Avg('rate'))

        if avg_rate['rate__avg'] is not None:
            return avg_rate['rate__avg']
        return 0

    def get_book_comments(self):
        return self.book_comment_set

    def get_abc(self):
        self.book_history_set


class Book_History(BookBase):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    rate = models.IntegerField(default=0)
    read_status = models.IntegerField(default=0)
    like_status = models.BooleanField(default=False)
    follow_status = models.BooleanField(default=False)

    class Meta:
        unique_together = [['user', 'book']]

    def get_follow_status(self):
        follow_status = Book.FOLLOW_STATUS[Book.FOLLOW]
        if self.follow_status == Book.FOLLOW:
            follow_status = Book.FOLLOW_STATUS[Book.UNFOLLOW]
        return follow_status

    def get_like_status(self):
        like_status = Book.LIKE_STATUS[Book.LIKE]
        if self.like_status == Book.LIKE:
            like_status = Book.LIKE_STATUS[Book.UNLIKE]
        return like_status


class Book_Request(BookBase):

    PENDING = 0
    ACCEPT = 1
    REJECT = 2

    STATUS_REQUEST = (
        'Pending',
        'Accept',
        'Reject'
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=500)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    note = models.TextField()
    price = models.IntegerField()
    status = models.IntegerField(default=0)

    def get_status(self):
        return self.STATUS_REQUEST[self.status]


class Book_Comment(BookBase):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    comment = models.TextField()
    parent_id = models.IntegerField(default=0)