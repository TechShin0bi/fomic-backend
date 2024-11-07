from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from . manager import UserManager
from common.models import BaseModel
from django.utils import timezone
import uuid
from django.utils.translation import gettext_lazy as _
from django.utils.timezone import now

class User(AbstractBaseUser, PermissionsMixin,BaseModel):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    first_name = models.CharField(_("first name"), max_length=150, blank=True)
    last_name = models.CharField(_("last name"), max_length=150, blank=True)
    email = models.EmailField(_("email address"), blank=True,unique=True)
    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_("Designates whether the user can log into this admin site."),
    )
    is_admin = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_("Designates whether the user can log into this admin site."),
    )
    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )
    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)
    image = models.ImageField(upload_to='profile_images/', null=True, blank=True,default="/assets/blue profile.png")
    balance = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    contact = models.CharField(max_length=15)
    referred_by = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True,related_name='referrals')

    objects = UserManager()

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name','last_name']

    def __str__(self):
        return self.email
    
    def update_balance_and_referred_users(self):
        """
        Updates the balance of the user based on their active plan, and then
        updates the plans of each referred user.
        """
        try:
            # Retrieve the active plan of the user
            user_plan = self.objects.get(user=self, is_active=True)
            plan = user_plan.plan  # Fetch the linked plan

            # Calculate days passed since the last process
            days_passed = (now().date() - user_plan.last_process.date()).days

            if days_passed > 0:
                # Calculate accumulated amount
                daily_revenue = plan.daily_revenue
                accumulated_amount = daily_revenue * days_passed

                # Update user balance
                self.balance += accumulated_amount
                self.save()

                # Update last_process date to today
                user_plan.last_process = now()
                user_plan.save()

                # Calculate referral bonus if applicable
                user_plan.calculate_referral_bonus()

            # Update referred users
            for referred_user in self.referrals.all():
                referred_user.update_balance_and_referred_users()

        except self.DoesNotExist:
            raise ValueError("Active user plan not found.")
    
class PasswordResetTokenCode(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reset_tokens')
    token = models.CharField(max_length=32)
    code = models.CharField(max_length=32)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    def is_valid(self):
        # Check if the token has expired
        return timezone.now() < self.expires_at