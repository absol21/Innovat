from rest_framework import serializers
from .. models import *
from django.contrib.auth import get_user_model
from django.db.models import Q

User = get_user_model()

class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']


class BookSerializer(serializers.ModelSerializer):
    language = serializers.SerializerMethodField(method_name='get_language')
    genre = GenreSerializer(many=True, allow_null=True)
    author = serializers.SerializerMethodField(method_name='get_author')
    owner = UserSerializer()

    class Meta:
        model = Book
        fields = '__all__'

    def get_language(self, obj):
        language = obj.language.language
        return language
    
    def get_author(self, obj):
        return obj.author.name


class AddBookSerializer(serializers.ModelSerializer):
    author = serializers.CharField()
    language = serializers.CharField()
    class Meta:
        model = Book
        fields = ['title', 'status', 'image', 'author', 'language', 'genre']

    def create(self, validated_data):
        user = self.context['request'].user
        if Author.objects.filter(name=validated_data['author']).exists():
            author = Author.objects.get(name=validated_data['author'])
        else:
            author = Author(
                name = validated_data['author']
            )
            author.save()
        
        if Language.objects.filter(language=validated_data['language']).exists():
            language = Language.objects.get(language=validated_data['language'])
        else:
            language = Language(
                language = validated_data['language']
            )
            language.save()

        book = Book(
            owner = user,
            title = validated_data['title'],
            status = validated_data['status'],
            image = validated_data['image'],
            language = language,
            author = author,
        )
        book.save()
        
        return book
    


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fiellds = '__all__'


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'


class RequestSeializer(serializers.ModelSerializer):
    class Meta:
        model = Request
        fields = '__all__'

