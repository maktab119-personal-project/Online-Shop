from django.contrib import admin

# Register your models here.
from django.contrib import admin
from core.models import ProxyEmployee  # فرض بر اینکه توی همون فایل هست یا ایمپورتش کردی
from django.contrib.auth.admin import UserAdmin

@admin.register(ProxyEmployee)
class EmployeeAdmin(UserAdmin):
    model = ProxyEmployee
    list_display = ('id', 'first_name', 'last_name', 'email', 'role')
    fieldsets = (
        ('Main Info', {'fields': ('first_name', 'last_name', 'email', 'phone', 'password')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'phone', 'password1', 'password2'),
        }),
    )
