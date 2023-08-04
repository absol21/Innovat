from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import *


router = DefaultRouter()

urlpatterns = [
    path('', include(router.urls)),
    path('all-books/', BookApiView.as_view(), name='allbooks'),
    path('add-book/', AddBookAPIView.as_view(), name='add-book')

]
