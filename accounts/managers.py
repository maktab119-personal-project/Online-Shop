from django.contrib.auth.base_user import BaseUserManager


class CustomerManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, phone, password=None, **extra_fields):
        if not email:
            raise ValueError("Users must have an email address")
        if not phone:
            raise ValueError("Users must have an phone number")
        email = self.normalize_email(email)
        user = self.model(phone=phone,email=email, first_name=first_name, last_name=last_name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name,phone,last_name, password, **extra_fields):
        extra_fields.setdefault('is_admin', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)
        user=self.create_user(email, first_name=first_name, phone=phone,last_name=last_name, password=password, **extra_fields)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        user.save(using=self._db)
        return user




