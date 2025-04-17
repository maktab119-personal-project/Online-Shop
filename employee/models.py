from django.contrib.auth.models import AbstractUser, Group, Permission
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
    groups = models.ManyToManyField(
        Group,
        related_name="employee_groups",
        blank=True,
        help_text="The groups this user belongs to.",
        verbose_name="groups"
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name="employee_permissions",
        blank=True,
        help_text="Specific permissions for this user.",
        verbose_name="user permissions"
    )
    def __str__(self):
        return self.get_role_display()

    objects = EmployeeManager()
