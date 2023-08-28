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
    permission_classes = [permissions.AllowAny]
    filterset_fields = ['genre', 'author', 'language'] 
    search_fields = ['title', 'author__name']
    serializer_class = BookSerializer

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Book.objects.exclude(owner=self.request.user)
        else:
            return Book.objects.all()
    

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
    serializer_class = EditMyBookSerilizer
    permission_classes = [IsOwner]


class UserBooksAPIView(generics.RetrieveAPIView):
    queryset = User.objects.all().prefetch_related('owned_books')
    serializer_class = UserBooksSerializer
    permission_classes = [permissions.IsAuthenticated]



class DeclineRequestAPIView(generics.UpdateAPIView,
                            generics.RetrieveAPIView):
    queryset = Request.objects.all().prefetch_related('requsted_books', 'sent_books')
    serializer_class = IncomingRequestsSerializer

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_declined = True
        instance.is_waiting = False
        instance.save()

        for book in instance.sent_books.all():
            book.status = 'доступно'
            book.save()
            
        return response.Response({"message": f"You declined request from user {instance.send_by.username}!"})
    

class AcceptRequestAPIView(generics.UpdateAPIView,
                           generics.RetrieveAPIView):
    queryset = Request.objects.all().prefetch_related('sent_books', 'sent_to')
    serializer_class = IncomingRequestsSerializer

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_accepted = True
        instance.is_waiting = False
        instance.save()

        for book in instance.sent_books.all():
            book.status = 'одобрено'
            book.save()
        
        for book in instance.requested_books.all():
            book.status = 'одобрено'
            book.save()

        return response.Response({"message": f"You accepted request from user {instance.send_by.username}!"})
    

class CancelRequestAPIView(generics.RetrieveAPIView,
                           generics.UpdateAPIView):
    queryset = Request.objects.all().prefetch_related('sent_books', 'sent_to')
    serializer_class = IncomingRequestsSerializer

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_accepted = False
        instance.is_agreed = False
        instance.is_canceled = True
        instance.save()

        for book in instance.sent_books.all():
            book.status = 'доступно'
            book.save()
        
        for book in instance.requested_books.all():
            book.status = 'доступно'
            book.save()

        return response.Response({"message": f"You canceled request from user {instance.send_by.username}!"}) 
    


#Подтверждение согласии место и время обмена
class ConfirmRequestAPIView(generics.RetrieveAPIView,
                            generics.UpdateAPIView):
    queryset = Request.objects.all().prefetch_related('sent_books', 'sent_to')
    serializer_class = IncomingRequestsSerializer

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_accepted = False
        instance.is_agreed = True
        instance.save()
        return response.Response({"message": f"You confirmed agreement with user {instance.send_by.username}!"}) 


#Подтверждение завершении обмена
class CompleteRequestAPIView(generics.RetrieveAPIView,
                             generics.UpdateAPIView):
    queryset = Request.objects.all().prefetch_related('sent_books', 'sent_to')
    serializer_class = IncomingRequestsSerializer

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_agreed = False
        instance.is_completed = True
        instance.save()
        return response.Response({"message": f"You confirmed completion of the exchange with user {instance.send_by.username}!"})