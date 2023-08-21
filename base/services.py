from django.core.exceptions import ValidationError

def get_path_upload_avatar(instance, filename):
    return f'avatar/{instance.id}/{filename}'

def get_path_upload_book(instance, file):
    return f'avatar/{instance.user.id}/{file}/'

def validate_image_size(file_obj):
    megabyte_limit = 2
    if file_obj.size > megabyte_limit * 1024 * 1024:
        raise ValidationError('Максимальный размер файла - 2 мегабайта')
