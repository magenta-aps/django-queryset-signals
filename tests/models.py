"""Test specific models."""

from django.db import models
from django_queryset_signals import (
    SignalQuerySet
)


class SignalUser(models.Model):
    """Imitates the default User model, but fires signals without patching."""
    objects = SignalQuerySet.as_manager()
    # We use these two data fields in our tests
    username = models.CharField(max_length=100, unique=True)
    last_name = models.CharField(max_length=100)
