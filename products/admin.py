from django.contrib import admin

# Register your models here.
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import Product, Category, Discount


# Register your models here.
class ProductsAdmin(admin.ModelAdmin):
    list_display = ['id','name','brand_name','category','price','stock','description','get_discount_price']
    ordering = ['id']
    search_fields = ['name']
    list_filter = ['category']
    def discount_price(self, obj):
        return obj.get_discount_price()
    discount_price.short_description = 'total price'

admin.site.register(Product, ProductsAdmin)

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'level']
admin.site.register(Category, CategoryAdmin)


class DiscountAdmin(admin.ModelAdmin):
    list_display = ['id','code','value','start_date','end_date']
admin.site.register(Discount, DiscountAdmin)



