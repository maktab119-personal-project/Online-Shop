from django.utils import timezone
from datetime import timedelta
import random
import phonenumbers
from django.core.validators import RegexValidator
from django.db import models
from django.contrib.auth.models import AbstractBaseUser , PermissionsMixin
from rest_framework.exceptions import ValidationError
from core.models import LogicalMixin
from employee.models import Employee
from .managers import CustomerManager


# Create your models here.

def validate_image_size(image):
    max_size_mb = 4
    if image.size > max_size_mb * 1024 * 1024:
        raise ValidationError(f"Image file size must be less than {max_size_mb} MB")


# def validate_phone_number(value):
#     try:
#         phone_number = phonenumbers.parse(value)
#         if not phonenumbers.is_valid_number(phone_number):
#             raise ValidationError("The phone number is not valid.")
#     except phonenumbers.phonenumberutil.NumberParseException:
#         raise ValidationError("The phone number is not valid.")
#


class Customer(AbstractBaseUser,PermissionsMixin, LogicalMixin):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(
        max_length=11,
        blank=True,
        verbose_name="Phone Number",
        validators=[
            RegexValidator(
                regex=r'^(0|0098|\+98)?9(0[1-5]|[1-3]\d|2[0-2]|9[0-9])\d{7}$',
                message="The entered phone number format is incorrect.",
            ),
        ],
    )
    # phone_number = models.CharField(
    #     max_length=15,
    #     unique=True,
    #     null=True,
    #     blank=True,
    #     validators=[validate_phone_number]
    # )
    address = models.ForeignKey('Address', on_delete=models.SET_NULL, null=True, blank=True, related_name="customer_address")
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name','phone']

    def __str__(self):
        return self.email



    objects = CustomerManager()


class Address(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True, blank=True, related_name="addresses")
    # employee = models.ForeignKey(Employee, on_delete=models.CASCADE, null=True, blank=True)
    country = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    province = models.CharField(max_length=100)
    street = models.CharField(max_length=255)
    number_plate = models.BigIntegerField()
    zipcode = models.CharField(max_length=20)


class OTP(LogicalMixin):
    user = models.OneToOneField(Customer, on_delete=models.CASCADE, related_name='otp')
    code = models.CharField(max_length=6)
    expires_at = models.DateTimeField()
    def __str__(self):
            return f'{self.user}, ( {self.otp} ),{self.created_at}'

    def generate_otp(self):
            self.otp = str(random.randint(100000, 999999))
            self.expires_at = timezone.now() + timedelta(minutes=2)
            self.save()

    def is_otp_valid(self):
            return timezone.now() <= self.expires_at