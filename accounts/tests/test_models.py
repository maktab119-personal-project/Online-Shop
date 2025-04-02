import pytest
from django.utils import timezone
from datetime import timedelta
from core.models import LogicalMixin
from employee.models import Employee
from accounts.models import Customer, Address

@pytest.mark.django_db
class TestCustomer:
    def test_create_customer(self):
        customer = Customer.objects.create_user(
            email="test@gmail.com",
            first_name="darya",
            last_name="gh",
            phone_number="+989123456789",
            password="secure1password"
        )
        assert customer.email == "test@gmail.com"
        assert customer.check_password("secure1password") is True
        assert customer.phone_number == "+989123456789"
        assert customer.first_name == "darya"
        assert customer.last_name == "gh"

    def test_create_admin(self):
        admin = Customer.objects.create_superuser(
            email="admin@gmail.com",
            first_name="Admin",
            last_name="User",
            phone_number="+989123456789",
            password="admin1password"
        )
        assert admin.is_staff is True
        assert admin.is_admin is True

@pytest.mark.django_db
class TestAddress:
    def test_create_address(self):
        customer = Customer.objects.create_user(
            email="user@gmail.com",
            first_name="darya",
            last_name="gh",
            phone_number="+989123456789",
            password="pass1word"
        )
        address = Address.objects.create(
            customer=customer,
            country="Iran",
            city="Tehran",
            province="Tehran",
            street="Valiasr",
            number_plate=16,
            zipcode="12345"
        )
        assert address.customer == customer
        assert address.city == "Tehran"
        assert address.province == "Tehran"
        assert address.street == "Valiasr"
        assert address.zipcode == "12345"



@pytest.mark.django_db
class TestEmployee:
    def test_create_employee(self):
        employee = Employee.objects.create_user(
            email="employee@example.com",
            first_name="shayan",
            last_name="ra",
            phone="+989123456789",
            password="secure1password",
            role="operator"
        )
        assert employee.email == "employee@example.com"
        assert employee.check_password("secure1password") is True
        assert employee.phone == "+989123456789"
        assert employee.first_name == "shayan"
        assert employee.last_name == "ra"
        assert employee.role == "operator"

    def test_create_manager(self):
        manager = Employee.objects.create_superuser(
            email="manager@example.com",
            first_name="iman",
            last_name="gh",
            phone="+989321654987",
            password="admin1password",
            role="manager"
        )
        assert manager.is_staff is True
        assert manager.is_superuser is True
        assert manager.role == "manager"
