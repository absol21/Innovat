from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import BookViewSet, AuthorViewSet, GenreViewSet


router = DefaultRouter()
router.register('books/', BookViewSet)
router.register('genres/', GenreViewSet)
router.register('Authors/', AuthorViewSet)


urlpatterns = [
    path('', include(router.urls)),

]
