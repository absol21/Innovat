from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from .tasks import send_activation_code_celery

User = get_user_model()


class GoogleAuth(serializers.Serializer):
    '''Сериализация данных от Google'''
    email = serializers.EmailField()
    token = serializers.CharField()


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(min_length=4, required=True, write_only=True)
    password_confirm = serializers.CharField(min_length=4, required=True, write_only=True)

    class Meta:
        model = User
        fields = ('email', 'password', 'password_confirm', 'username', 'number', 'city', 'avatar')

    def validate(self, attrs):
        password = attrs.get("password")
        password_confirm = attrs.pop("password_confirm")
        if password != password_confirm:
            raise serializers.ValidationError("Passwords don't match!")
        return attrs

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        send_activation_code_celery(user.email, user.activation_code)
        return user

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(min_length=4, required=True)
    new_password = serializers.CharField(min_length=4, required=True)
    new_password_confirm = serializers.CharField(min_length=4, required=True)

    def validate_old_password(self, old_password):
        request = self.context.get('request')
        user = request.user
        if not user.check_password(old_password):
            raise serializers.ValidationError(
                'Вы ввели не корректный пароль'
            )
        return old_password
    
    def validate(self, data):
        old_pass = data.get('old_password')
        new_pass1 = data.get('new_password')
        new_pass2 = data.get('new_password_confirm')
        if new_pass1 != new_pass2:
            raise serializers.ValidationError(
                'Пароли не совпадают'
            )
        if old_pass == new_pass1:
            raise serializers.ValidationError(
                'Этот пароль использовался ранее'
            )
        return data
    
    def set_new_password(self):
        new_pass = self.validated_data.get('new_password')
        user = self.context.get('request').user
        user.set_password(new_pass)
        user.save()


class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.CharField(required=True)

    def validate_email(self, email):
        if not User.objects.filter(email=email).exists():
            raise serializers.ValidationError(
                'Такого пользователя нет'
            )
        return email

    def send_verification_email(self):
        email = self.validated_data.get('email')
        user = User.objects.get(email=email)
        user.create_activation_code()
        send_mail(
            'Восстановление пароля',
            f'Ваш код восстановлления {user.activation_code}',
            'test@gmail.com',
            [user.email]
        )
        

class ForgotPasswordCompleteSerializer(serializers.Serializer):
    email = serializers.CharField(required=True)
    code = serializers.CharField(required=True)
    password = serializers.CharField(min_length=4, required=True)
    password_confirm = serializers.CharField(min_length=4, required=True)

    def validate(self, data):

        email = data.get('email')
        code = data.get('code')
        password = data.get('password')
        password_confirm = data.get('password_confirm')

        print('success data', data)

        if not User.objects.filter(email=email, activation_code=code).exists():
            raise serializers.ValidationError(
                'Пользователь не найден'
            )
        
        
        if password != password_confirm:
            raise serializers.ValidationError(
               'Пароли не совпадают' 
            )
        
        return data
    
    def set_new_password(self):
        print(self)
        email = self.validated_data.get('email')
        print(email)
        password = self.validated_data.get('password')
        user = User.objects.get(email=email)
        user.set_password(password)
        user.activation_code = ''
        user.save()