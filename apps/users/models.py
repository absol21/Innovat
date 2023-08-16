from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, User
from django.utils.crypto import get_random_string
from base.services import get_path_upload_avatar, validate_image_size
from django.core.validators import FileExtensionValidator

from main import settings


class UserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('Email field is required')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.create_activation_code()
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        if not email:
            raise ValueError('Email field is required')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True
        user.save()
        return user

class Rating(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    rating = models.DecimalField(max_digits=5, decimal_places=2, default=0)


class User(AbstractBaseUser):

    username = models.CharField(max_length=60)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=12, blank=True, null=True)
    location = models.CharField(max_length=60,)
    avatar = models.ImageField(
        upload_to=get_path_upload_avatar,
        blank=True,
        null=True,
        validators=[validate_image_size]
                                )
    user_rating = models.OneToOneField(Rating, on_delete=models.CASCADE, related_name='user_rating')
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    activation_code = models.CharField(max_length=10, blank=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self) -> str:
        return f'{self.email} -> {self.id}'
    
    def has_module_perms(self, app_label):
        return self.is_staff
    
    def has_perm(self, perm, obj=None):
        return self.is_staff

    def create_activation_code(self):
        code = get_random_string(length=10, allowed_chars='0123456789')
        self.activation_code = code
        self.save()







