from django.db import models
from Authentication.models import User
import uuid

class Payment(models.Model):
    PAYMENT_METHOD_CHOICES = [
        ('eSewa', 'eSewa'),
        ('Khalti', 'Khalti'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    transaction_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    status = models.CharField(max_length=20, default='Pending')  # Can be Pending, Success, Failed
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Optional fields
    response_data = models.TextField(blank=True, null=True)  # Store full response (e.g., JSON)

    def __str__(self):
        return f"{self.user.username} | {self.method} | {self.status} | {self.amount}"
