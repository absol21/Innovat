from rest_framework.routers import DefaultRouter
from django.urls import path, include
from apps.exchange.api.views import *


router = DefaultRouter()

urlpatterns = [
    path('', include(router.urls)),
    path('all-books/', BookApiView.as_view(), name='allbooks'),
    path('add-book/', AddBookAPIView.as_view(), name='add-book'),
    path('book-detail/<int:pk>/', BookDetailAPIView.as_view(), name='book-detail'),
    path('send-request-user/<int:pk>/', SendRequestAPIView.as_view(), name='send-request'),
    path('my-requests/', MyRequestsAPIView.as_view(), name='my-requests'),
    path('edit-my-request/<int:pk>/', EditMyRequestsAPIView.as_view(), name='edit-my-request'),
    path('incoming-requests/', IncomingRequestsAPIView.as_view(), name='incoming-requests'),
    path('incoming-request/<int:pk>/', IncomingRequestsAPIView.as_view(), name='incoming-request'),
    path('my-books/', MyBooksAPIView.as_view(), name='my-books'),
    path('edit-my-book/<int:pk>/', EditMyBookAPIView.as_view(), name='edit-my-book'),
    path('all-books-user/<int:pk>/', UserBooksAPIView.as_view(), name='user-books'),
    path('my-books/', MyBooksListView.as_view(), name='my-books-list'),
    path('my-books/<int:pk>/', MyBooksDetailView.as_view(), name='my-books-detail'),

]
