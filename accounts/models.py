import phonenumbers
from django.core.validators import RegexValidator
from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from rest_framework.exceptions import ValidationError
from core.models import LogicalMixin
from employee.models import Employee
from .managers import CustomerManager


# Create your models here.

def validate_image_size(image):
    max_size_mb = 4
    if image.size > max_size_mb * 1024 * 1024:
        raise ValidationError(f"Image file size must be less than {max_size_mb} MB")


def validate_phone_number(value):
    """
    اعتبارسنجی شماره تلفن با استفاده از کتابخانه phonenumbers.
    """
    try:
        phone_number = phonenumbers.parse(value)
        if not phonenumbers.is_valid_number(phone_number):
            raise ValidationError("شماره تلفن وارد شده معتبر نیست.")
    except phonenumbers.phonenumberutil.NumberParseException:
        raise ValidationError("شماره تلفن وارد شده معتبر نیست.")


class Customer(AbstractBaseUser, LogicalMixin):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    # phone = models.CharField(
    #     max_length=11,
    #     blank=True,
    #     verbose_name="Phone Number",
    #     validators=[
    #         RegexValidator(
    #             regex=r'^(0|0098|\+98)?9(0[1-5]|[1-3]\d|2[0-2]|9[0-9])\d{7}$',
    #             message="The entered phone number format is incorrect.",
    #         ),
    #     ],
    # )
    phone_number = models.CharField(
        max_length=15,
        unique=True,
        null=True,
        blank=True,
        validators=[validate_phone_number]  # اعتبارسنجی شماره تلفن
    )
    address = models.ForeignKey('Address', on_delete=models.SET_NULL, null=True, blank=True, related_name="customer_address")
    # registration_date = models.DateTimeField(auto_now_add=True)
    # update_at = models.DateTimeField(auto_now=True)
    # is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name']

    def __str__(self):
        return self.email

    @property
    def is_staff(self):
        return self.is_admin

    objects = CustomerManager()


class Address(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True, blank=True, related_name="addresses")
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, null=True, blank=True)
    country = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    province = models.CharField(max_length=100)
    street = models.CharField(max_length=255)
    number_plate = models.BigIntegerField()
    zipcode = models.CharField(max_length=20)
