from django.shortcuts import render
from rest_framework import viewsets
from .serializers import BookSerializer, GenreSerializer, AuthorSerializer
from .models import Book, Author, Genre

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

