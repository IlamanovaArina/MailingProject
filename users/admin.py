from django.contrib import admin

from users.models import User


# Register your models here.
@admin.register(User)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'avatar', 'phone', 'country',)
    list_filter = ('email',)
    search_fields = ('email', 'id')