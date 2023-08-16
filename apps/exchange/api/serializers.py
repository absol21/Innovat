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
    

class BookDetailUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'phone_number', 'location', 'avatar']
    

class BookDetailSerializer(serializers.ModelSerializer):
    owner = BookDetailUserSerializer()
    class Meta:
        model = Book
        fields = '__all__'


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
            language = language,
            author = author,
        )
        if 'image' in validated_data:
            book.image = validated_data['image']

        book.save()
        for i in validated_data['genre']:
            book.genre.add(i)
        
        return book
    


class SentBooksPrimaryKeyRelatedField(serializers.PrimaryKeyRelatedField):
    def get_queryset(self):
        current_user = self.context['request'].user
        queryset = super().get_queryset()
        return queryset.filter(owner=current_user)
    

class RequestedBooksPrimaryKeyRelatedField(serializers.PrimaryKeyRelatedField):
    def get_queryset(self):
        current_object = self.context['view'].get_object()
        queryset = super().get_queryset()
        return queryset.filter(owner=current_object)


class SendRequestSerializer(serializers.ModelSerializer):
    send_to = UserSerializer(read_only=True)
    sent_books = SentBooksPrimaryKeyRelatedField(many=True, queryset=Book.objects.all())
    requested_books = RequestedBooksPrimaryKeyRelatedField(many=True, queryset=Book.objects.all())

    class Meta:
        model = Request
        fields = ['send_to', 'sent_books', 'requested_books']


    def create(self, validated_data):
        sent_books = validated_data['sent_books']
        requested_books = validated_data['requested_books']

        request = Request(
            sent_to = self.context['view'].get_object(),
            send_by = self.context['request'].user,
            is_waiting = True
        )
        request.save()

        for books in sent_books:
            request.sent_books.add(books)

        for books in requested_books:
            request.requested_books.add(books)

        return request
    


class MyRequestsSerializer(serializers.ModelSerializer):
    sent_books = BookSerializer(many=True, allow_null=True)
    requested_books = BookSerializer(many=True, allow_null=True)
    sent_to = UserSerializer()
    send_by = UserSerializer()

    class Meta:
        model = Request
        fields = '__all__'



class EditMyRequestsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Request
        fields = ['sent_books', 'requested_books']


class IncomingRequestsSerializer(serializers.ModelSerializer):
    sent_books = BookSerializer(many=True, allow_null=True)
    requested_books = BookSerializer(many=True, allow_null=True)
    send_by = UserSerializer()

    class Meta:
        model = Request
        fields = ['sent_books', 'requested_books', 'send_by', 'created_at']



class MyBooksSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'
        read_only_fields = ['owner']


class UserBooksSerializer(serializers.ModelSerializer):
    owned_books = MyBooksSerializer(many=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'phone_number', 'location', 'avatar', 'owned_books']