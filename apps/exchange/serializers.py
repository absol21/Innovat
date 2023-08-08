from rest_framework import serializers
from . import models

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Book
        fields = '__all__'


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Author
        fields = ('name',)


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Genre
        fields = '__all__'


class RequestSeializer(serializers.ModelSerializer):
    class Meta:
        model = models.Request
        fields = '__all__'

# class RequestSerializer(serializers.Serializer):
#     requester = serializers.CharField()