from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils.crypto import get_random_string
from base.services import get_path_upload_avatar, validate_image_size


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


class User(AbstractBaseUser):
    username = models.CharField(max_length=60, unique=True)
    email = models.EmailField(unique=True)
    number = models.CharField(max_length=12, blank=True, null=True)
    city = models.CharField(max_length=60,)
    avatar = models.ImageField(
        upload_to=get_path_upload_avatar,
        blank=True,
        null=True,
        validators=[validate_image_size]
    )
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    activation_code = models.CharField(max_length=10, blank=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

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


class Rating(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ratings_given')
    rating = models.PositiveSmallIntegerField()
    username = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ratings_recieved', to_field='username')

    def __str__(self):
        return f'{self.rating} -> {self.user}'