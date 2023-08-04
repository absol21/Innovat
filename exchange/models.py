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
    genre = models.ManyToManyField(Genre, related_name='book_genre')
    language = models.ForeignKey(Language, on_delete=models.CASCADE, related_name='book_language')
    is_available = models.BooleanField(default=True)

    statuses = [
        ('Б/у', 'Б/у'),
        ('Новый', 'Новый'),
    ]
    status = models.CharField(max_length=5, choices=statuses)
    image = models.ImageField(
        upload_to=get_path_upload_book,
        blank=True,
        null=True,
        validators=[FileExtensionValidator(allowed_extensions=['jpg']), validate_image_size]
    )

    def __str__(self) -> str:
        return self.title
    
    class Meta:
        ordering = ['-title', 'owner']
    

class Request(models.Model):
    book1 = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='exchanges_as_book1')
    book2 = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='exchanges_as_book2')
    sent_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name='send_to')
    send_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='send_by')
    created_at = models.DateTimeField(auto_now_add=True)

    
    wait_status = models.BooleanField(default=False)
    acceptt_status = models.BooleanField(default=False)
    agree_status = models.BooleanField(default=False)
    complete_status = models.BooleanField(default=False)
    decline_status = models.BooleanField(default=False)
    cancle_status = models.BooleanField(default=False)

    
    STATUS_CHOICES = [
    ('pending_confirmation', 'Ожидание подтверждения'),
    ('request_accepted', 'Запрос принят'),
    ('exchange_details_confirmed', 'Детали обмена согласованы'),
    ('exchange_completed', 'Обмен завершен'),
    ('request_rejected', 'Отклонен'),
    ('request_cancelled', 'Отменен'),
]

    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='pending_confirmation')

class Rating(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ratings_given')
    rating = models.PositiveSmallIntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ratings_recieved')

    def __str__(self):
        return f'{self.rating} -> {self.user}'
    
    # def __str__(self) -> str:
    #     return self.books

# class ExchangeRequest(models.Model):
#     requester = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_requests')
#     requested_book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='exchange_requests')
#     message = models.TextField()
#     created_at = models.DateTimeField(auto_now_add=True)
#     is_accepted = models.BooleanField(default=False)

# class Exchange(models.Model):
#     user1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='exchanges_as_user1')
#     user2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='exchanges_as_user2')
#     book1 = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='exchanges_as_book1')
#     book2 = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='exchanges_as_book2')
#     is_completed = models.BooleanField(default=False)
#     rating_user1 = models.PositiveIntegerField(blank=True, null=True)
#     rating_user2 = models.PositiveIntegerField(blank=True, null=True)
#     review_user1 = models.TextField(blank=True)
#     review_user2 = models.TextField(blank=True)
#     completed_at = models.DateTimeField(blank=True, null=True)