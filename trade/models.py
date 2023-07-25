from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Author(models.Model):
    name = models.CharField(max_length=60)

    def __str__(self) -> str:
        return self.name
    

class Genre(models.Model):
    title = models.CharField(max_length=60)

    def __str__(self) -> str:
        return self.title


class Book(models.Model):
    title = models.CharField(max_length=100)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owner')
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='author')
    genre = models.ManyToManyField(Genre, related_name='genre')
    statuses = [
        ('Б/у', 'Б/у'),
        ('Новый', 'Новый'),
    ]
    status = models.CharField(max_length=5, choices=statuses)

    def __str__(self) -> str:
        return self.title
    

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
