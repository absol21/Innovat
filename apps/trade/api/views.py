from django.shortcuts import render
from rest_framework import viewsets, generics
from django.db.models import Q
from rest_framework import response, permissions
from .serializers import *
from ..models import Book, Author, Genre
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

class BookApiView(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    filterset_fields = ['genre', 'author', 'language'] 
    search_fields = ['title', 'author__name']


class AddBookAPIView(generics.CreateAPIView):
    queryset = Book.objects.all()
    serializer_class = AddBookSerializer