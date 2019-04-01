from django.contrib import admin
from .models import CustomUser


class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'username', 'avatar', 'age', 'is_staff',)
    search_fields = ('id', 'username',)
    ordering = ('id',)


admin.site.register(CustomUser, CustomUserAdmin)
