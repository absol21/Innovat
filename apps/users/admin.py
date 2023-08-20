from django.db.models import Avg
from django.contrib import admin
from .models import User

class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'username', 'city', 'number', 'avatar', 'is_active', 'is_staff', 'get_rating')

    def get_rating(self, obj):
        return obj.ratings_given.aggregate(Avg('rating'))['rating__avg']

    get_rating.short_description = 'Rating'

admin.site.register(User, UserAdmin)
