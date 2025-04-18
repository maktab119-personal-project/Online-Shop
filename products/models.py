from django.db import models
from django.utils.timezone import now
from rest_framework.exceptions import ValidationError

from core.models import LogicalMixin


# Create your models here.

def validate_image_size(image):
    MAX_SIZE_MB = 4
    if image.size > MAX_SIZE_MB * 1024 * 1024: #MAX
        raise ValidationError(f"Image file size must be less than {MAX_SIZE_MB} MB")


class Product(LogicalMixin):
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    discounts = models.ManyToManyField('Discount', blank=True)
    name = models.CharField(max_length=255)
    brand_name = models.CharField(max_length=255 ,default='Unknown')
    description = models.TextField()
    img = models.ImageField(upload_to='products/', validators=[validate_image_size])
    price = models.BigIntegerField(default=1000)
    stock = models.BigIntegerField(default=0)


    def __str__(self):
        return f"{self.name} - {self.discounts}{self.get_discount_price()}"

    def get_active_discounts(self):
        today = now().date()
        return self.discounts.filter(
            start_date__lte=today,
            end_date__gte=today,
            # code__isnull=True  # فقط تخفیف‌های عمومی برای محصول
        )

    def get_discount_price(self):
        """Calculate price after applying best available discount"""
        active_discounts = self.get_active_discounts()
        print(">> Active Discounts:", active_discounts)
        if not active_discounts.exists():
            return self.price

        best_discount = None
        best_discount_value = 0

        for discount in active_discounts:
            if discount.is_percentage:
                current_value = self.price * discount.value / 100
            else:
                current_value = discount.value

            if current_value > best_discount_value:
                best_discount_value = current_value
                best_discount = discount

        if best_discount.is_percentage:
            final_price = self.price * (1 - best_discount.value / 100)
        else:
            final_price = self.price - best_discount.value

        return max(round(final_price), 0)

    # Alias for serializer compatibility
    get_discounted_price = get_discount_price

class Category(LogicalMixin):
    Level_choices = [
        (1, 'Main-Category'),
        (2, 'Sub-Category'),
        (3, 'Sub-Subcategory'),
    ]
    name = models.CharField(max_length=255)
    parent = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        verbose_name="children",
    )
    level = models.PositiveSmallIntegerField(choices=Level_choices, verbose_name="Category_Level", default=1)

    def __str__(self):
        return self.name


class Discount(LogicalMixin):
    code = models.CharField(max_length=50, unique=True, null=True, blank=True)
    value = models.BigIntegerField(help_text="If percentage, enter number like 20 for 20%")
    is_percentage = models.BooleanField(default=True)
    start_date = models.DateField()
    end_date = models.DateField()

    def is_valid(self):
        today = now().date()
        return self.start_date <= today <= self.end_date

    def __str__(self):
        typ = "%" if self.is_percentage else "TOMAN"
        return f"{self.code or 'PUBLIC'} - {self.value}{typ}"



class Review(LogicalMixin):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='review_product')
    rating = models.SmallIntegerField()
    comment = models.TextField()
    review_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.product.name} - {self.rating}/5"
