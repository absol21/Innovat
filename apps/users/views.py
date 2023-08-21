from rest_framework.views import APIView

from .serializers import (
    RegisterSerializer,
    ChangePasswordSerializer,
    ForgotPasswordSerializer,
    ForgotPasswordCompleteSerializer, 
    EditAvatarSerializer, 
    EditProfileSerializer
    )
from .models import User
from .permissions import IsActivePermissions

from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view
from rest_framework.response import Response

from rest_framework.parsers import MultiPartParser


# from . import serializers
# from rest_framework.exceptions import AuthenticationFailed
# from .google import check_google_auth

from base.services import validate_image_size
    

class EditAvatarView(APIView):
    parser_classes = [MultiPartParser]

    @swagger_auto_schema(request_body=EditAvatarSerializer())
    def patch(self, request):
        data = request.data
        avatar_file = data['avatar']
        serializer = EditAvatarSerializer(data=data)

        if avatar_file:
            validate_image_size(avatar_file)

        if serializer.is_valid(raise_exception=True):
            user = request.user  # Получаем текущего пользователя
            if user.avatar:
                user.avatar.delete()  # Удаляем старый аватар, если есть
            user.avatar = avatar_file  # Устанавливаем новый аватар
            user.save()  # Сохраняем пользователя

            return Response('Аватар изменен', status=201)
        else:
            return Response(serializer.errors, status=400)
       


class EditProfileView(APIView):
    @swagger_auto_schema(request_body=EditProfileSerializer())
    def patch(self, request):
        data = request.data
        serializer = EditProfileSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        return Response('Successfully edited', 201)

# '''Google views'''
# def google_login(request):
#     """страница входа через Google"""
#     return render(request, 'templates/google_login.html')

# @api_view(["POST"])
# def google_auth(request):
#     '''Подтверждение авторизации через Google'''
#     google_data = serializers.GoogleAuth(data=request.data)
#     if google_data.is_valid():
#         token = check_google_auth(google_data.data)
#         return Response(token)
#     else:
#         return Response({'error': 'bad data Google'}, status=403)



class RegisterView(APIView):
    @swagger_auto_schema(request_body=RegisterSerializer())
    def post(self, request):
        data = request.data
        serializer = RegisterSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        return Response("Successfully registered", 201)

class ActivationView(APIView):
    def get(self, request, email, activation_code):
        user = User.objects.filter(email=email, activation_code=activation_code).first()
        if not user:
            return Response("User doesn't exist", 400)
        user.activation_code = ''
        user.is_active = True
        user.save()
        return Response('Activated', 200)


class ChangePasswordView(APIView):
    permission_classes = [IsActivePermissions]
    
    @swagger_auto_schema(request_body=ChangePasswordSerializer())
    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data, context={'request': request})
        if serializer.is_valid(raise_exception = True):
            serializer.set_new_password()
            return Response('Status: 200. Пароль успешно обнавлен')
         

class ForgotPasswordView(APIView):
    @swagger_auto_schema(request_body=ForgotPasswordSerializer())
    def post(self, request):
        serializer = ForgotPasswordSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.send_verification_email()
            return Response('Вы выслали сообщение для восстановления')
        

class ForgotPasswordCompleteView(APIView):
    @swagger_auto_schema(request_body=ForgotPasswordCompleteSerializer())
    def post(self, request):
        serializer = ForgotPasswordCompleteSerializer(data=request.data) 
        if serializer.is_valid(raise_exception=True):
            serializer.set_new_password()
            return Response('Пароль успешно изменен')
        

from rest_framework.viewsets import ModelViewSet
from .serializers import Rating, RatingSerializer
from rest_framework import permissions

# class RatingView(ModelViewSet):
#     queryset = Rating.objects.all()
#     serializer_class = RatingSerializer
#     permission_classes = [permissions.IsAuthenticated]



# class RatingViewApi(APIView):
#     def get(self, request):
#         author = request.author
#         rating = Rating.objects.all(author=author, username=request.username, rating=request.rating)
#         if not rating:
#             return Response("you didn't rated this user")
#         else:
#             return rating

#     def post(self, request):
#         serializer = RatingSerializer(data=request.data)
#         if serializer.is_valid(raise_exception=True):
#             serializer.save()
#         return Response('raited', 200)
    
#     def patch(self, request):
#         data = request.data
#         serializer = RatingSerializer(data=data)
#         if serializer.is_valid(raise_exception=True):
#             serializer.save()
#         return Response('Successfully edited', 201)
    
#     def delete(self, request):
#         author = request.author
#         rating = Rating.objects.get(author=author, rating=request.rating, username=request.username)
#         if rating:
#             rating.delete()
#         else:
#             return Response("You did't ratetd this user")


class RatingViewApi(APIView):
    def post(self, request):
        serializer = RatingSerializer(data=request.data, context={'request': request})

        if serializer.is_valid():
            serializer.save()
            return Response("Rated successfully", status=201)
        return Response(serializer.errors, status=201)

    def patch(self, request):
        user = request.user
        username = request.data.get('username')
        
        try:
            rating = Rating.objects.get(author=user, username=username)
        except Rating.DoesNotExist:
            return Response("You haven't rated this user yet", status=401)

        serializer = RatingSerializer(rating, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response("Rating updated successfully", status=200)
        return Response(serializer.errors, status=401)

    def delete(self, request):
        user = request.user
        username = request.data.get('username')

        try:
            rating = Rating.objects.get(author=user, username=username)
        except Rating.DoesNotExist:
            return Response("You haven't rated this user yet", status=404)

        rating.delete()
        return Response("Rating deleted successfully", status=204)

    def get(self, request):
        user = request.user
        username = request.query_params.get('username')

        try:
            rating = Rating.objects.get(author=user, username=username)
        except Rating.DoesNotExist:
            return Response("You haven't rated this user yet", status=404)

        serializer = RatingSerializer(rating)
        return Response(serializer.data, status=200)
