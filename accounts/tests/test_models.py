
import pytest
from django.utils import timezone
from datetime import timedelta

from django.utils.timezone import now

from core.models import LogicalMixin
from employee.models import Employee
from accounts.models import Customer, Address
from products.models import Product, Category
from orders.models import Order, OrderItem, Payment

@pytest.mark.django_db
class TestCustomer:
    def test_create_customer(self):
        customer = Customer.objects.create_user(
            email="test@gmail.com",
            first_name="darya",
            last_name="gh",
            phone="+9891234567",
            password="secure1password"
        )
        assert customer.email == "test@gmail.com"
        assert customer.check_password("secure1password") is True
        assert customer.phone == "+9891234567"
        assert customer.first_name == "darya"
        assert customer.last_name == "gh"

    def test_create_admin(self):
        admin = Customer.objects.create_superuser(
            email="admin@gmail.com",
            first_name="Admin",
            last_name="User",
            phone="+9891234567",
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
            phone="+9891234567",
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
            phone="+9891234567",
            password="secure1password",
            role="operator"
        )
        assert employee.email == "employee@example.com"
        assert employee.check_password("secure1password") is True
        assert employee.phone == "+9891234567"
        assert employee.first_name == "shayan"
        assert employee.last_name == "ra"
        assert employee.role == "operator"

    def test_create_manager(self):
        manager = Employee.objects.create_superuser(
            email="manager@example.com",
            first_name="iman",
            last_name="gh",
            phone="+9893216549",
            password="admin1password",
            role="manager"
        )
        assert manager.is_staff is True
        assert manager.is_superuser is True
        assert manager.role == "manager"



@pytest.mark.django_db
class TestOrder:
    def test_create_order(self):
        customer = Customer.objects.create_user(
            email="hi@gmail.com",
            first_name="darya",
            last_name="gh",
            phone="+9891234567",
            password="secure1password"
        )
        address = Address.objects.create(
            customer=customer,
            street="123 Test St",
            city="Test City",
            number_plate="12",
            zipcode="12345"
        )
        order = Order.objects.create(
            customer=customer,
            address=address,
            order_date=now().date(),
            total_price=100000,
            status='pending'
        )
        assert order.customer == customer
        assert order.address == address
        assert order.total_price == 100000
        assert order.status == 'pending'

    def test_create_order_item(self):
        customer = Customer.objects.create_user(
            email="test@gmail.com",
            first_name="baran",
            last_name="gh",
            phone="+9891234567",
            password="secure1password"
        )
        address = Address.objects.create(
            customer=customer,
            street="123 Test St",
            city="Test City",
            number_plate="12",
            zipcode="12345"
        )
        order = Order.objects.create(
            customer=customer,
            address=address,
            order_date=now().date(),
            total_price=100000,
            status='pending'
        )
        category = Category.objects.create(name="Electronics")
        product = Product.objects.create(
            name="Test Product",
            price=50000,
            category=category,
            stock=10
        )
        order_item = OrderItem.objects.create(
            order=order,
            quantity=2,
            subtotal=100000
        )
        order_item.product.add(product)
        assert order_item.order == order
        assert order_item.quantity == 2
        assert order_item.subtotal == 100000
        assert product in order_item.product.all()

    def test_create_payment(self):
        customer = Customer.objects.create_user(
            email="test@gmail.com",
            first_name="darya",
            last_name="gh",
            phone="+9891234567",
            password="secure1password"
        )
        address = Address.objects.create(
            customer=customer,
            street="123 Test St",
            city="Test City",
            number_plate="12",
            zipcode="12345"
        )
        order = Order.objects.create(
            customer=customer,
            address=address,
            order_date=now().date(),
            total_price=100000,
            status='pending'
        )
        payment = Payment.objects.create(
            order=order,
            customer=customer,
            amount=100000,
            payment_method='credit_card',
            payment_date_time=now()
        )
        assert payment.order == order
        assert payment.customer == customer
        assert payment.amount == 100000
        assert payment.payment_method == 'credit_card'
