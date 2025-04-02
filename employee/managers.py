from django.db import models
from django.contrib.auth.models import BaseUserManager
from django.core.management.base import BaseCommand


class EmployeeManager(BaseUserManager):
    def create_user(self, email, role, password=None, **extra_fields):
        if not email:
            raise ValueError("Users must have an email address")

        email = self.normalize_email(email)
        user = self.model(email=email, role=role, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, role, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, role, password, **extra_fields)




# class Command(BaseCommand):
#     help = 'Create admin user'
#
#     def handle(self, *args, **options):
#         email = input('Enter email: ')
#
#         if Employee.objects.filter(email=email).exists():
#             self.stdout.write(self.style.ERROR('User already exists.'))
#             return
#
#         user = Employee.objects.create_superuser(email=email, password="admin123")
#         self.stdout.write(self.style.SUCCESS(f"Successfully created admin user: {email}"))

