from django.db import models
from django.utils import timezone
from . managers import AppManager

class BaseModel(models.Model):
    # Soft delete fields
    id = models.UUIDField(primary_key=True)
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)

    # Timestamp fields
    created_at = models.DateTimeField(auto_now_add=True)  # Set only on creation
    updated_at = models.DateTimeField(auto_now=True)  # Updated every save
    
    objects = AppManager()
    all_objects = models.Manager()
    
    class Meta:
        abstract = True  # This ensures the model is used only as a base class

    def delete(self, using=None, keep_parents=False):
        """Soft delete the object by setting `is_deleted` to True."""
        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.save(using=using)

    def hard_delete(self, using=None):
        """Permanently delete the object from the database."""
        super().delete(using=using)

    def restore(self):
        """Restore a soft-deleted object."""
        self.is_deleted = False
        self.deleted_at = None
        self.save()

    @classmethod
    def get_queryset(cls):
        """Return only non-deleted objects."""
        return super().get_queryset().filter(is_deleted=False)

    def save(self, *args, **kwargs):
        """Override save to ensure `updated_at` is correctly updated."""
        if self.is_deleted and not self.deleted_at:
            self.deleted_at = timezone.now()
        super().save(*args, **kwargs)
