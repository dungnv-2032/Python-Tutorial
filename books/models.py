from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User
from django.db.models import Avg
from django.urls import reverse


class Category(models.Model):
    name = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Book(models.Model):

    UNREAD = 0
    READING = 1
    READ = 2
    READ_STATUS = (
        (UNREAD, 'Unread'),
        (READING, 'Reading'),
        (READ, 'Read'),
    )

    UNFOLLOW = 0
    FOLLOW = 1
    FOLLOW_STATUS = (
        (UNFOLLOW, 'Unfollow'),
        (FOLLOW, 'Follow')
    )

    LIKE_STATUS = (
        (0, 'Unlike'),
        (1, 'Like')
    )

    RATE = (
        (0, 'Unrate'),
        (1, 'Bad'),
        (2, 'Normal'),
        (3, 'Good'),
        (4, 'Very Good'),
        (5, 'Super Good')
    )

    name = models.CharField(max_length=500)
    description = models.TextField(null=True)
    author = models.CharField(max_length=200)
    price = models.IntegerField(default=0)
    category = models.ForeignKey(Category, on_delete=models.SET(0))
    publish_date = models.DateField()
    image = models.ImageField(verbose_name='image', upload_to='images/')
    number_page = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def count_follow(self):
        return Book_History.objects.filter(
            book=self,
            follow_status=self.FOLLOW_STATUS[1][0]
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


class Book_History(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    rate = models.IntegerField(default=0)
    read_status = models.IntegerField(default=0)
    like_status = models.BooleanField(default=False)
    follow_status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = [['user', 'book']]


class Book_Request(models.Model):

    PENDING = 0
    ACCEPT = 1
    REJECT = 2

    STATUS_REQUEST = [
        'Pending',
        'Accept',
        'Reject'
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=500)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    note = models.TextField()
    price = models.IntegerField()
    status = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_status(self):
        return self.STATUS_REQUEST[self.status]


class Book_Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    comment = models.TextField()
    parent_id = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
