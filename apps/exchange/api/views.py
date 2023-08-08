from django.shortcuts import render
from rest_framework import viewsets, generics, mixins
from django.db.models import Q
from rest_framework import response, permissions
from .serializers import *
from ..models import Book, Author, Genre
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from django.contrib.auth import get_user_model
from .permissions import *


User = get_user_model()



class BookApiView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ['genre', 'author', 'language'] 
    search_fields = ['title', 'author__name']

    def get_queryset(self):
        return Book.objects.all()
    
    def list(self, request, *args, **kwargs):
        current_user = request.user
        queryset = self.get_queryset().exclude(owner=current_user)
        serializer = BookSerializer(queryset, many=True)
        return response.Response(serializer.data)
    


class BookDetailAPIView(generics.RetrieveAPIView):
    queryset = Book.objects.all()
    serializer_class = BookDetailSerializer
    permission_classes = [permissions.IsAuthenticated]


class AddBookAPIView(generics.CreateAPIView):
    queryset = Book.objects.all()
    serializer_class = AddBookSerializer
    permission_classes = [permissions.IsAuthenticated]  


class SendRequestAPIView(generics.RetrieveAPIView,
                         generics.CreateAPIView):
    queryset = User.objects.all().prefetch_related('send_to')

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return UserSerializer
        elif self.request.method == 'POST':
            return SendRequestSerializer

    
class MyRequestsAPIView(generics.ListAPIView):
    serializer_class = MyRequestsSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Request.objects.all().prefetch_related('sent_books', 'requested_books', 'sent_to', 'send_by')
    
    def list(self, request, *args, **kwargs):
        current_user = request.user
        queryset = self.get_queryset().filter(send_by=current_user)
        serializer = MyRequestsSerializer(queryset, many=True)
        return response.Response(serializer.data)
    


class EditMyRequestsAPIView(generics.RetrieveAPIView, 
                            generics.DestroyAPIView,
                            generics.UpdateAPIView):
    queryset = Request.objects.all().prefetch_related('sent_books', 'requested_books', 'sent_to', 'send_by')
    serializer_class = EditMyRequestsSerializer
    permission_classes = [IsSender]


class IncomingRequestsAPIView(generics.ListAPIView,
                              generics.RetrieveAPIView):
    serializer_class = IncomingRequestsSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Request.objects.all().prefetch_related('sent_books', 'requested_books', 'sent_to', 'send_by')
    
    def list(self, request, *args, **kwargs):
        current_user = request.user
        queryset = self.get_queryset().filter(sent_to=current_user)
        serializer = IncomingRequestsSerializer(queryset, many=True)
        return response.Response(serializer.data) 
    


class MyBooksAPIView(generics.ListAPIView):
    serializer_class = MyBooksSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Book.objects.all()
    
    def list(self, request, *args, **kwargs):
        current_user = request.user
        queryset = self.get_queryset().filter(owner=current_user)
        serializer = MyBooksSerializer(queryset, many=True)
        return response.Response(serializer.data)
    

class EditMyBookAPIView(generics.RetrieveAPIView,
                        generics.UpdateAPIView,
                        generics.DestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = MyBooksSerializer
    permission_classes = [IsOwner]


class UserBooksAPIView(generics.RetrieveAPIView):
    queryset = User.objects.all().prefetch_related('owned_books')
    serializer_class = UserBooksSerializer
    permission_classes = [permissions.IsAuthenticated]