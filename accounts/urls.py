from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from products.views import ProductListCreateView, CategoryListView, ProductRetrieveUpdateDeleteView, \
    DiscountCreateAPIView
from . import views
from django.views.generic import TemplateView

from .views import RequestOTPView

urlpatterns = [
    path('', TemplateView.as_view(template_name='home.html'), name='home'),

    path('signup/', TemplateView.as_view(template_name="signup.html"), name="signup"),
    path('api/signup/', views.SignupView.as_view(), name='signup_api'),
    path('api/login/',views.LoginView.as_view(), name='login_api'),
    path('login/', TemplateView.as_view(template_name="login.html"), name="login"),
    path('api/otp/', RequestOTPView.as_view(), name='request-otp'),

    path('products/', TemplateView.as_view(template_name="products.html"), name="products"),
    path('api/products/', ProductListCreateView.as_view(), name='product-list'),
    path('api/products/<int:id>/', ProductRetrieveUpdateDeleteView.as_view(), name='product-detail'),
    path('api/categories/', CategoryListView.as_view(), name='category-list'),


    path('profile/', TemplateView.as_view(template_name="profile.html"), name="profile"),
    path('discounts/create/', DiscountCreateAPIView.as_view(), name='discount-create'),

    # path('profile/<int:id>/', TemplateView.as_view(template_name="profile.html"), name="profile_id"),
    # path('profile/<int:user_id>/', views.profile_view, name='profile'),

    # TOKEN JWT
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
