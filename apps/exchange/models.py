from django.db import models
from django.contrib.auth import get_user_model
from base.services import get_path_upload_book, validate_image_size
from django.core.validators import FileExtensionValidator


User = get_user_model()

class Author(models.Model):
    name = models.CharField(max_length=60)

    def __str__(self) -> str:
        return self.name
    
    class Meta:
        ordering = ['-name']


class Genre(models.Model):
    title = models.CharField(max_length=60)

    def __str__(self) -> str:
        return self.title

    class Meta:
        ordering = ['-title']


class Language(models.Model):
    language = models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.language

    class Meta:
        ordering = ['-language']


class Book(models.Model):
    title = models.CharField(max_length=100)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owned_books')
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='book_author')
    genre = models.ForeignKey(Genre, on_delete=models.SET_NULL, null=True, related_name='book_genre')
    language = models.ForeignKey(Language, on_delete=models.CASCADE, related_name='book_language')
    
    status = [('одобрено', 'Одобрено'),
              ('рассматривается', 'Рассматривается'),
              ('доступно', 'Доступно'),
              ]
    status = models.CharField(max_length=15, choices=status, default='доступно')
    description = models.TextField(blank=True, null=True)
    condition = models.CharField(max_length=25)
    
    image = models.ImageField(
        upload_to=get_path_upload_book,
        blank=True,
        null=True,
    )

    def __str__(self) -> str:
        return self.title
    
    class Meta:
        ordering = ['-title', 'owner']
    

class Request(models.Model):
    sent_books = models.ManyToManyField(Book, related_name='sent_books')
    requested_books = models.ManyToManyField(Book, related_name='requsted_books')
    sent_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name='send_to')
    send_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='send_by')
    created_at = models.DateTimeField(auto_now_add=True)
    is_waiting = models.BooleanField(default=False)
    is_accepted = models.BooleanField(default=False)
    is_agreed = models.BooleanField(default=False)
    is_completed = models.BooleanField(default=False)
    is_declined = models.BooleanField(default=False)
    is_canceled = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.send_by.username
    
    class Meta:
        ordering = ['-id']
