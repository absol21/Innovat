from django.shortcuts import render
from rest_framework import viewsets
from .serializers import BookSerializer, GenreSerializer, AuthorSerializer, RequestSeializer
from .models import Book, Author, Genre
from rest_framework import generics
from rest_framework.views import APIView

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer

class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer

class RequestView(APIView):
    def post(self, request):
        request = RequestSeializer(data=request.data)
        