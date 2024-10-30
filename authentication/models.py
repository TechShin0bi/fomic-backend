from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from . manager import UserManager
from common.models import BaseModel
from django.utils import timezone
import uuid
from django.utils.translation import gettext_lazy as _

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
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name','last_name']

    def __str__(self):
        return self.email