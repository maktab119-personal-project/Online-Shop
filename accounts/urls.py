from django.urls import path
from . import views
from django.views.generic import TemplateView

urlpatterns = [
    path('', TemplateView.as_view(template_name='home.html'), name='home'),

    path('signup/', TemplateView.as_view(template_name="signup.html"), name="signup"),
    path('login/', TemplateView.as_view(template_name="login.html"), name="login"),
    path('Products/', TemplateView.as_view(template_name="product.html"), name="Product"),
    path('Profile/', TemplateView.as_view(template_name="profile.html"), name="Profile"),
]
