from django.db import models
from MainApp.models import OrderPlaced
# Create your models here.


# Define payment methods
PAYMENT_METHOD_CHOICES = [
    ('online','Online Payment'),   
    ('offline', 'Offline Payment')
]

# Define payment status choices
PAYMENT_STATUS_CHOICES = [
    ('pending', 'Pending'),
    ('completed', 'Completed'),
    ('failed', 'Failed'),
    ('cancelled', 'Cancelled')
]


class Payment(models.Model):
    order = models.OneToOneField(OrderPlaced, on_delete=models.CASCADE)
    payment_method = models.CharField(
        max_length=20, choices=PAYMENT_METHOD_CHOICES)
    payment_status = models.CharField(
        max_length=20, choices=PAYMENT_STATUS_CHOICES, default='pending')
    payment_date = models.DateTimeField(auto_now_add=True)
    transaction_id = models.CharField(
        max_length=255, unique=True, null=True, blank=True)
    invoice_no = models.CharField(max_length=20, unique=True, blank=True, null=True)

    def __str__(self):
        return str(self.id)