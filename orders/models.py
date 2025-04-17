from django.db import models

from accounts.models import Customer, Address
from products.models import Product


# Create your models here.

class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    payment = models.ForeignKey('Payment', on_delete=models.CASCADE, null=True, blank=True,related_name='order_payment')
    order_date = models.DateField()
    total_price = models.BigIntegerField()
    status = models.CharField(max_length=50,
                              choices=[('pending', 'Pending'), ('completed', 'Completed'), ('canceled', 'Canceled')])


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    subtotal = models.BigIntegerField()


class Payment(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE,related_name='payment_order')
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    amount = models.BigIntegerField()
    payment_method = models.CharField(max_length=50, choices=[('credit_card', 'Credit Card'), ('paypal', 'PayPal'), ('cash', 'Cash')])
    payment_date_time = models.DateTimeField()