from django.conf import settings
from django.db import models
from django.utils import timezone
from common.models import BaseModel  # Assuming you use your base model

User = settings.AUTH_USER_MODEL  # Refers to your User model

class Deposit(BaseModel):
    code = models.CharField(max_length=50, unique=True)  # Code for the deposit
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(default=timezone.now)
    status = models.CharField(
        max_length=10,
        choices=[('pending', 'Pending'), ('completed', 'Completed')],
        default='pending'
    )
    is_validated = models.BooleanField(default=False)  # Validation flag
    validated_by = models.ForeignKey(
        User, null=True, blank=True, on_delete=models.SET_NULL,
        related_name='validated_deposits',
        limit_choices_to={'isAdmin': True}  # Only admins can validate
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='deposits')

    def __str__(self):
        return f'Deposit {self.code} - {self.amount}'


class Withdrawal(BaseModel):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(default=timezone.now)
    is_validated = models.BooleanField(default=False)  # Validation flag
    validated_by = models.ForeignKey(
        User, null=True, blank=True, on_delete=models.SET_NULL,
        related_name='validated_withdrawals',
        limit_choices_to={'isAdmin': True}  # Only admins can validate
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='withdrawals')

    def __str__(self):
        return f'Withdrawal - {self.amount}'
