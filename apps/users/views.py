from .serializers import (
    RegisterSerializer,
    ChangePasswordSerializer,
    ForgotPasswordSerializer,
    ForgotPasswordCompleteSerializer, 
    EditProfileSerializer,
    EditAvatarSerializer,
    ProfileSerializer
    )
from .models import User
from .permissions import IsActivePermissions
from base.services import validate_image_size
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework import permissions



class MyProfileAPIView(generics.ListAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return User.objects.filter(username=self.request.user)
    

class ProfileView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = ProfileSerializer

    def get(self, request, pk=None):
        if pk is None:
            profiles = self.get_queryset()
            serializer = self.get_serializer(profiles, many=True)
            return Response(serializer.data)
        else:
            profile = self.get_object()
            serializer = self.get_serializer(profile)
            return Response(serializer.data)


class EditAvatarView(APIView):
    parser_classes = [MultiPartParser]

    @swagger_auto_schema(request_body=EditAvatarSerializer())
    def patch(self, request):
        serializer = EditAvatarSerializer(data=request.data, context={'request': request})

        if serializer.is_valid():
            serializer.save()
            return Response('Аватар изменен', status=201)
        else:
            return Response(serializer.errors, status=400)


class EditProfileView(APIView):
    @swagger_auto_schema(request_body=EditProfileSerializer())
    def patch(self, request):
        data = request.data
        serializer = EditProfileSerializer(request.user, data=data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        return Response('Successfully edited', 201)


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

    # def get(self, request):
    #     user = request.user
    #     username = request.query_params.get('username')

    #     try:
    #         rating = Rating.objects.get(author=user, username=username)
    #     except Rating.DoesNotExist:
    #         return Response("You haven't rated this user yet", status=404)

    #     serializer = RatingSerializer(rating)
    #     return Response(serializer.data, status=200)
