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
    genre = GenreSerializer()
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
        fields = ['id', 'username', 'number', 'city', 'avatar']
    

class BookDetailSerializer(serializers.ModelSerializer):
    owner = BookDetailUserSerializer()
    class Meta:
        model = Book
        fields = '__all__'


class AddBookSerializer(serializers.ModelSerializer):
    author = serializers.CharField()
    language = serializers.CharField()
    genre = serializers.CharField()
    class Meta:
        model = Book
        fields = ['title', 'condition', 'image', 'author', 'language', 'genre', 'description']

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

        
        if Genre.objects.filter(title=validated_data['genre']).exists():
            genre = Genre.objects.get(title=validated_data['genre'])
        else:
            genre = Genre(
                title = validated_data['genre']
            )
            genre.save()

        book = Book(
            owner = user,
            title = validated_data['title'],
            language = language,
            author = author,
            genre = genre,
            condition = validated_data['condition'],
            image = validated_data['image'],
            description = validated_data['description']
        )
        if 'image' in validated_data:
            book.image = validated_data['image']

        if 'description' in validated_data:
            book.description = validated_data['description']

        book.save()
        print(book)
        
        return book


class SentBooksPrimaryKeyRelatedField(serializers.PrimaryKeyRelatedField):
    def get_queryset(self):
        current_user = self.context['request'].user
        queryset = super().get_queryset()
        return queryset.filter(owner=current_user).exclude(status='одобрено')
    

class RequestedBooksPrimaryKeyRelatedField(serializers.PrimaryKeyRelatedField):
    def get_queryset(self):
        current_object = self.context['view'].get_object()
        queryset = super().get_queryset()
        return queryset.filter(owner=current_object).exclude(status='одобрено')


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

        for book in sent_books:
            request.sent_books.add(book)
            book.status = 'рассматривается'
            book.save()

        for book in requested_books:
            request.requested_books.add(book)

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
    genre = GenreSerializer()
    class Meta:
        model = Book
        fields = '__all__'
        read_only_fields = ['owner']


class EditMyBookSerilizer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'
        read_only_fields = ['owner']


class UserBooksSerializer(serializers.ModelSerializer):
    owned_books = MyBooksSerializer(many=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'number', 'city', 'avatar', 'owned_books']