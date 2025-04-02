from django.contrib.auth.models import AbstractUser
from django.db import models
from employee.managers import EmployeeManager


# Create your models here.

class Employee(AbstractUser):
    ROLE_CHOICES = [
        ('manager', 'مدیر محصولات'),
        ('supervisor', 'ناظر'),
        ('operator', 'اپراتور'),
    ]
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    password = models.CharField(max_length=255)
    role = models.CharField(max_length=50, choices=ROLE_CHOICES)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.get_role_display()

    objects = EmployeeManager()
