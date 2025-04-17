import logging
from django.core.mail import EmailMessage
from django.conf import settings
from django.shortcuts import redirect
from .models import Customer

logger = logging.getLogger(__name__)

def send_otp_email(email, otp_code):
    try:
        user = Customer.objects.get(email=email)
    except Customer.DoesNotExist:
        logger.error(f"User with email {email} not found.")
        return

    if not user:
        logger.error(f"User with email {email} is not an account. OTP will not be sent.")
        return

    subject = 'Your OTP Code'
    email_body = f'Hi {user.email}, your OTP code is: {otp_code}'
    from_email = settings.EMAIL_HOST_USER

    email_message = EmailMessage(subject=subject, body=email_body, from_email=from_email, to=[email])
    try:
        email_message.send(fail_silently=False)
        logger.info(f"OTP sent successfully to {email}.")
    except Exception as e:
        logger.error(f"Error sending email to {email}: {e}")

def is_staff_user(user):
    """بررسی اینکه آیا کاربر ادمین (staff) هست یا نه"""
    return user and getattr(user, 'is_staff', False)
