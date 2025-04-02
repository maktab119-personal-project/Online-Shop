from django.contrib import admin

from accounts.forms import UserChangeForm, UserCreationForm
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import Customer

# Register your models here.
class CustomerAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    list_display = ['id','first_name','last_name','email']
    ordering = ['id']
    search_fields = ['email']
    readonly_fields = ['last_login']
    # filter_horizontal = ['groups','user_permissions']

    fieldsets = (
        ('Main', {'fields':('first_name','last_name','phone', 'email','password')}),
        ('permissions',{'fields':('is_active','is_verified','is_staff','is_superuser','groups','last_login','user_permissions')}),
    )

    add_fieldsets = (
        (None, {'fields':('first_name','phone','email','password1','password2')}),
    )

