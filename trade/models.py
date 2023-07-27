from django.db import models
from django.contrib.auth import get_user_model
from base.services import get_path_upload_avatar, validate_image_size
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
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owner')
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='author')
    genre = models.ManyToManyField(Genre, related_name='genre')
    language = models.ForeignKey(Language, on_delete=models.CASCADE, related_name='languages')
    statuses = [
        ('Б/у', 'Б/у'),
        ('Новый', 'Новый'),
    ]
    status = models.CharField(max_length=5, choices=statuses)
    image = models.ImageField(
        upload_to=get_path_upload_avatar,
        blank=True,
        null=True,
        validators=[FileExtensionValidator(allowed_extensions=['jpg']), validate_image_size]
    )

    def __str__(self) -> str:
        return self.title
    
    class Meta:
        ordering = ['-title', 'owner']


class Request(models.Model):
    books = models.ManyToManyField(Book)
    sent_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name='send_to')
    send_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='send_by')
    statuses =[
        ('wait', 'waiting'),
        ('accepted', 'accepted'),
        ('agreed', 'agreed'),
        ('completed', 'completed'),
        ('declined', 'declined'),
        ('canceled', 'canceled')
    ]
    status = models.CharField(max_length=10, choices=statuses)

    def __str__(self) -> str:
        return self.books

class Genre(models.Model):
    title = models.CharField(max_length=60)

    def __str__(self) -> str:
        return self.title

    class Meta:
        ordering = ['-title']

class Library(models.Model):
    books = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='books')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owner')

    def __str__(self) -> str:
        return self.books
