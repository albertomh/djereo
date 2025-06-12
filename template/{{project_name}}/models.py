import uuid

from django.db import models
from django.utils import timezone


class UuidModel(models.Model):
    id: models.UUIDField = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False
    )

    class Meta:
        abstract = True


class CreatedAtModel(models.Model):
    created_at: models.DateTimeField = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class UpdatedAtModel(models.Model):
    updated_at: models.DateTimeField = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class DeletedAtModel(models.Model):
    deleted_at: models.DateTimeField = models.DateTimeField(
        blank=True, null=True, default=None, editable=False
    )

    def soft_delete(self):
        self.deleted_at = timezone.now()
        self.save(update_fields=["deleted_at"])

    def restore(self):
        self.deleted_at = None
        self.save(update_fields=["deleted_at"])

    class Meta:
        abstract = True
