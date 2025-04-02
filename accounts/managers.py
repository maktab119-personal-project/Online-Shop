from django.contrib.auth.base_user import BaseUserManager


class CustomerManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, phone_number, password=None, **extra_fields):
        if not email:
            raise ValueError("Users must have an email address")
        if not phone_number:
            raise ValueError("Users must have an phone number")
        email = self.normalize_email(email)
        user = self.model(phone_number=phone_number,email=email, first_name=first_name, last_name=last_name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name, phone_number, password=None, **extra_fields):
        extra_fields.setdefault('is_admin', True)
        user = self.create_user(email, first_name, last_name, phone_number, password, **extra_fields)
        return user




