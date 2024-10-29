from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now

class PlanCategory(models.TextChoices):
    CATEGORY_1 = '1', 'Category 1'
    CATEGORY_2 = '2', 'Category 2'

class Plan(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    daily_revenue = models.DecimalField(max_digits=10, decimal_places=2)
    duration = models.PositiveIntegerField(help_text="Duration in days")
    category = models.CharField(
        max_length=1,
        choices=PlanCategory.choices,
        default=PlanCategory.CATEGORY_1,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.get_category_display()})"

class UserPlan(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_plans')
    plan = models.ForeignKey(Plan, on_delete=models.SET_NULL, null=True, related_name='user_plans')
    is_active = models.BooleanField(default=True)  # Track if this is the current active plan
    last_process = models.DateTimeField(default=now)  # Store the last process date

    def __str__(self):
        return f"{self.user.username}'s Plan: {self.plan.name if self.plan else 'No Plan'}"

    class Meta:
        unique_together = ('user', 'is_active')  # Ensure only one active plan per user
