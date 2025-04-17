from rest_framework import serializers
from .models import Customer , Address
from django.core.cache import cache
from .email import send_otp_email
from django.utils.crypto import get_random_string
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError



class SignupSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = Customer
        fields = [
            'email', 'phone', 'password', 'password2',
            'first_name', 'last_name'
        ]
        extra_kwargs = {
            'password': {'write_only': True},
            'phone': {'required': True},
            'email': {'required': True},
            'first_name': {'required': True},
            'last_name': {'required': True}
        }

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError("Passwords must match.")
        return data
    def validate_email(self, value):
        if Customer.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already registered.")
        return value

    def create(self, validated_data):
        password = validated_data.pop('password')
        validated_data.pop('password2')

        user = Customer.objects.create_user(password=password,**validated_data)
        return user

class VerifyOTPSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField(max_length=6)


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    login_type = serializers.ChoiceField(choices=['password', 'otp'], required=True)
    password = serializers.CharField(write_only=True, required=False)
    otp = serializers.CharField(write_only=True, required=False)

    def validate(self, data):
        email = data.get("email")
        password = data.get("password")
        otp = data.get("otp")

        try:
            user = Customer.objects.get(email=email)
        except Customer.DoesNotExist:
            raise serializers.ValidationError("User not found.")

        if password:
            user = authenticate(email=email, password=password)
            if not user:
                raise serializers.ValidationError("Invalid credentials.")
        elif otp:
            stored_otp = cache.get(f'otp_{email}')
            if not stored_otp or stored_otp != otp:
                raise serializers.ValidationError("Invalid or expired OTP.")
            cache.delete(f'otp_{email}')
        else:
            raise serializers.ValidationError("Provide either password or OTP.")

        if not user.is_active:
            raise serializers.ValidationError("User account is disabled.")

        return {"user": user}


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['id', 'first_name','last_name','email', 'phone']

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)
