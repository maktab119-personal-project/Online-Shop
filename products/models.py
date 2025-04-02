from django.db import models
from django.utils.timezone import now
from rest_framework.exceptions import ValidationError

from core.models import LogicalMixin


# Create your models here.

def validate_image_size(image):
    max_size_mb = 4
    if image.size > max_size_mb * 1024 * 1024:
        raise ValidationError(f"Image file size must be less than {max_size_mb} MB")


class Product(models.Model):
    category = models.ForeignKey('Category', on_delete=models.CASCADE,limit_choices_to={'level': 3})
    discounts = models.ManyToManyField('Discount', blank=True)
    reviews = models.ForeignKey('Review', on_delete=models.CASCADE, null=True, blank=True,related_name='product_reviews')
    name = models.CharField(max_length=255)
    brand_name = models.CharField(max_length=255 ,default='Unknown')
    description = models.TextField()
    img = models.ImageField(upload_to='products/', validators=[validate_image_size])
    price = models.BigIntegerField()
    stock = models.BigIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.name


class Category(models.Model):
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



class Discount(models.Model):
    code = models.CharField(max_length=50, unique=True, null=True, blank=True)
    value = models.BigIntegerField()
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return f"{self.code} - {self.value}"


class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='review_product')
    rating = models.SmallIntegerField()
    comment = models.TextField()
    review_date = models.DateField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.product.name} - {self.rating}/5"
