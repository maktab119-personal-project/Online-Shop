from django.contrib import admin

# Register your models here.
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import Product, Category


# Register your models here.
class ProductsAdmin(admin.ModelAdmin):
    list_display = ['id','name','brand_name','category','price','stock','description']
    ordering = ['id']
    search_fields = ['name']
    list_filter = ['category']


admin.site.register(Product, ProductsAdmin)

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'level']
admin.site.register(Category, CategoryAdmin)

