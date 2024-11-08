from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from . manager import UserManager
from common.models import BaseModel
from django.utils import timezone
import uuid
from django.utils.translation import gettext_lazy as _
from django.utils.timezone import now
from decimal import Decimal



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
    plan = models.ForeignKey("plan.Plan",null=True,blank=True,on_delete=models.RESTRICT)
    last_balance_processed = models.DateTimeField(blank=True , null=True)
    processed_refereal = models.DateTimeField(blank=True , null=True)
    objects = UserManager()

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name','last_name']

    def __str__(self):
        return self.email
    
    def update_balance_and_referred_users(self):
        """
        Updates the balance of a user based on the daily revenue of their active plan. 
        Calculates the number of days since the last balance update and applies the accumulated revenue.
        Recursively updates the balance for any referred users.
        
        Parameters:
        - user (User): The user instance to update.
        """
        # Ensure the user has an active plan
        if not self.plan:
            # Calculate the days passed since the last balance update
            last_processed_date = self.last_balance_processed.date() if self.last_balance_processed else now().date()
            days_passed = (now().date() - last_processed_date).days

            if days_passed > 0:
                # Calculate the total accumulated amount based on daily revenue and days passed
                accumulated_amount = self.plan.daily_revenue * Decimal(days_passed)
                
                # Update the user's balance and the last balance processed date
                self.balance += accumulated_amount
                self.last_balance_processed = now()  # Set last processed time to current time
                self.save()
            # Recursively update the balance for each referred user
            for referred_user in self.referrals.all():
                referred_user.update_balance_and_referred_users()
            
    def calculate_referral_bonus(user):
        """
        Calculates and applies the referral bonus to the referrer of the given user, if applicable.
        Assumes a 20% bonus of the daily revenue from the user's plan.
        
        Parameters:
        - user (User): The user for whom to apply the referral bonus.
        """
        referral_bonus_percentage = Decimal(0.2)  # 20% bonus

        # Ensure the user has a referrer and an active plan
        if user.referred_by and user.plan and not user.referred_by.processed_refereal:
            referral_bonus = user.plan.daily_revenue * referral_bonus_percentage
            user.referred_by.balance += referral_bonus
            user.referred_by.processed_refereal = now()  # Update the referral processing time
            user.referred_by.save()
    
class PasswordResetTokenCode(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reset_tokens')
    token = models.CharField(max_length=32)
    code = models.CharField(max_length=32)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    def is_valid(self):
        # Check if the token has expired
        return timezone.now() < self.expires_at