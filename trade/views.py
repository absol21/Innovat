from django.shortcuts import render
from rest_framework import viewsets
from .serializers import BookSerializer, Book

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
