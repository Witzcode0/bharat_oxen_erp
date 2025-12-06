from django.contrib import admin
from apps.master.models import User


# Register your models here.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('fullname', 'username', 'email', 'mobile', 'is_active', 'created_at')
    search_fields = ('fullname', 'username', 'email', 'mobile')
    list_filter = ('is_active', 'created_at')
    ordering = ('-created_at',)