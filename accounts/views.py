import logging
from rest_framework.permissions import AllowAny
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
# Create your views here.
from rest_framework.generics import GenericAPIView
from django.core.cache import cache
from django.utils.crypto import get_random_string
from .models import Customer
from .email import send_otp_email, is_staff_user
from .serializers import SignupSerializer, LoginSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework import status
import random
from django.contrib.auth.models import update_last_login



class SignupView(GenericAPIView):
    serializer_class = SignupSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        user.save()
        user_data = serializer.data

        return Response({
            'data': user_data,
            'message': f'Hi {user_data["email"]}, your account has been successfully created and verified.'
        }, status=status.HTTP_201_CREATED)


logger = logging.getLogger(__name__)


class LoginView(GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            email = request.data.get("email")
            password = request.data.get("password")
            otp = request.data.get("otp")
            login_type = request.data.get("login_type")

            if not email:
                return Response({"message": "Email is required."}, status=status.HTTP_400_BAD_REQUEST)

            try:
                user = Customer.objects.get(email=email)
            except Customer.DoesNotExist:
                return Response({"message": "User not found."}, status=status.HTTP_404_NOT_FOUND)

            if login_type == 'password':
                if not password:
                    return Response({"message": "Password is required for password login."},
                                    status=status.HTTP_400_BAD_REQUEST)
                serializer = self.get_serializer(data=request.data)
                serializer.is_valid(raise_exception=True)
                user = serializer.validated_data['user']

            elif login_type == 'otp':
                if not otp:
                    # send otp code to email
                    otp_code = str(random.randint(100000, 999999))
                    cache.set(f'otp_{email}', otp_code, timeout=300)
                    send_otp_email(email, otp_code)
                    return Response({"message": "OTP has been sent to your email."}, status=status.HTTP_200_OK)

                # check otp code
                cached_otp = cache.get(f'otp_{email}')
                if not cached_otp or cached_otp != otp:
                    return Response({"message": "Invalid or expired OTP."}, status=status.HTTP_400_BAD_REQUEST)
                cache.delete(f'otp_{email}')

            else:
                return Response({"message": "Invalid login_type. Use 'password' or 'otp'."},
                                status=status.HTTP_400_BAD_REQUEST)

            refresh = RefreshToken.for_user(user)
            update_last_login(None, user)  # <-- این خطو اضافه کن

            is_staff = is_staff_user(user)

            return Response({
                "refresh": str(refresh),
                "access": str(refresh.access_token),
                "is_staff": is_staff,
                "user_id": user.id,
                "message": "Login successful"
            }, status=status.HTTP_200_OK)

        except Exception as e:
            logger.exception("Login error")
            return Response({"message": "Internal server error."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class RequestOTPView(GenericAPIView):

    def post(self, request):
        email = request.data.get("email")

        if not email:
            return Response({"message": "Email is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = Customer.objects.get(email=email)
        except Customer.DoesNotExist:
            return Response({"message": "User not found."}, status=status.HTTP_404_NOT_FOUND)

        otp_code = str(random.randint(100000, 999999))
        cache.set(f'otp_{email}', otp_code, timeout=300)
        send_otp_email(email, otp_code)

        return Response({"message": "OTP has been sent to your email."}, status=status.HTTP_200_OK)



# from django.views.generic import TemplateView
#
# class ProfileView(TemplateView):
#     template_name = 'profile.html'
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         user_id = self.kwargs.get('id')
#
#         # اگر id موجود بود، اون یوزر رو بیار، در غیر اینصورت یوزر لاگین‌شده
#         if user_id:
#             context['profile_user'] = Customer.objects.get(id=user_id)
#         else:
#             context['profile_user'] = self.request.user
#
#         return context


@login_required
def profile_view(request, user_id):
    user = get_object_or_404(Customer, id=user_id)
    return render(request, 'profile.html', {'user': user, 'user_id': user.id})
