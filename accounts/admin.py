from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'role', 'is_staff', 'is_superuser', 'date_joined')
    list_filter = ('role', 'is_staff', 'is_superuser', 'date_joined')
    search_fields = ('username', 'email')
    ordering = ('-date_joined',)
    fieldsets = UserAdmin.fieldsets + (
        ('Extra', {'fields': ('role', 'bio')}),
    )
