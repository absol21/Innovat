from django.contrib import admin
from . import models

@admin.register(models.Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'owner', 'image', 'author']

admin.site.register(models.Author)
admin.site.register(models.Genre)
admin.site.register(models.Language)
admin.site.register(models.Request)