"""
This module is imported on app ready (see __init__).
"""

from django.db.models.query import QuerySet
from django.dispatch import Signal
from django.conf import settings

# TODO: Create a generic 'data-changed' signal
# pre_save = Signal(providing_args=["queryset", "objs", "batch_size"])
# post_save = Signal(providing_args=["queryset", "objs", "batch_size"])

# TODO: Consider providing results into post signals
# TODO: Consider pk list versions


pre_bulk_create = Signal(providing_args=["queryset", "objs", "batch_size"])
post_bulk_create = Signal(providing_args=["queryset", "objs", "batch_size"])

def _bulk_create(self, objs, batch_size=None):
    pre_bulk_create.send(sender=self.model, queryset=self, objs=objs, batch_size=batch_size)
    return_val = getattr(self, 'raw_bulk_create')(objs=objs, batch_size=batch_size)
    post_bulk_create.send(sender=self.model, queryset=self, objs=objs, batch_size=batch_size)
    return return_val


pre_get_or_create = Signal(providing_args=["queryset", "defaults", "kwargs"])
post_get_or_create = Signal(providing_args=["queryset", "defaults", "kwargs"])

def _get_or_create(self, defaults=None, **kwargs):
    pre_get_or_create.send(sender=self.model, queryset=self, defaults=defaults, **kwargs)
    return_val = getattr(self, 'raw_get_or_create')(defaults=defaults, **kwargs)
    post_get_or_create.send(sender=self.model, queryset=self, defaults=defaults, **kwargs)
    return return_val


pre_update_or_create = Signal(providing_args=["queryset", "defaults", "kwargs"])
post_update_or_create = Signal(providing_args=["queryset", "defaults", "kwargs"])

def _update_or_create(self, defaults=None, **kwargs):
    pre_update_or_create.send(sender=self.model, queryset=self, defaults=defaults, **kwargs)
    return_val = getattr(self, 'raw_update_or_create')(defaults=defaults, **kwargs)
    post_update_or_create.send(sender=self.model, queryset=self, defaults=defaults, **kwargs)
    return return_val


pre_create = Signal(providing_args=["queryset", "kwargs"])
post_create = Signal(providing_args=["queryset", "kwargs"])

def _create(self, **kwargs):
    pre_create.send(sender=self.model, queryset=self, **kwargs)
    return_val = getattr(self, 'raw_create')(**kwargs)
    post_create.send(sender=self.model, queryset=self, **kwargs)
    return return_val


pre_delete = Signal(providing_args=["queryset"])
post_delete = Signal(providing_args=["queryset"])

def _delete(self):
    pre_delete.send(sender=self.model, queryset=self)
    return_val = getattr(self, 'raw_delete')()
    post_delete.send(sender=self.model, queryset=self)
    return return_val


pre_update = Signal(providing_args=["queryset", "kwargs"])
post_update = Signal(providing_args=["queryset", "kwargs"])

def _update(self, **kwargs):
    pre_update.send(sender=self.model, queryset=self, **kwargs)
    return_val = getattr(self, 'raw_update')(**kwargs)
    post_update.send(sender=self.model, queryset=self, **kwargs)
    return return_val


# Trigger queryset delete signal on model-delete
from django.dispatch import receiver
from django.db.models.signals import (
    pre_delete as django_pre_delete,
    post_delete as django_post_delete,
)
@receiver(django_pre_delete)
def pre_delete_to_qs_pre_delete(sender, instance, *args, **kwargs):
    pre_delete.send(sender=sender, queryset=sender.objects.filter(pk=instance.pk))

@receiver(django_post_delete)
def post_delete_to_qs_post_delete(sender, instance, *args, **kwargs):
    post_delete.send(sender=sender, queryset=sender.objects.filter(pk=instance.pk))

# Trigger queryset create / update / whatever on model-save
from django.db.models.signals import (
    pre_save as django_pre_save,
    post_save as django_post_save,
)
@receiver(django_pre_save)
def pre_save_to_qs_signals(sender, instance, *args, **kwargs):
    if instance.pk is None:
        # Does not exist
        pass
    else:
        # Does exist
        pass
    print args
    print kwargs

@receiver(django_post_save)
def post_save_to_qs_signals(sender, instance, *args, **kwargs):
    if instance.pk is None:
        # Does not exist
        pass
    else:
        # Does exist
        pass
    print args
    print kwargs


class SignalQuerySet(QuerySet):
    # https://docs.djangoproject.com/en/1.11/_modules/django/db/models/query/#QuerySet

    def bulk_create(self, objs, batch_size=None):
        pre_bulk_create.send(sender=self.model, queryset=self, objs=objs, batch_size=batch_size)
        return_val = super(SignalQuerySet, self).bulk_create(objs=objs, batch_size=batch_size)
        post_bulk_create.send(sender=self.model, queryset=self, objs=objs, batch_size=batch_size)
        return return_val

    def get_or_create(self, defaults=None, **kwargs):
        pre_get_or_create.send(sender=self.model, queryset=self, defaults=defaults, **kwargs)
        return_val = super(SignalQuerySet, self).get_or_create(defaults=defaults, **kwargs)
        post_get_or_create.send(sender=self.model, queryset=self, defaults=defaults, **kwargs)
        return return_val

    def update_or_create(self, defaults=None, **kwargs):
        pre_update_or_create.send(sender=self.model, queryset=self, defaults=defaults, **kwargs)
        return_val = super(SignalQuerySet, self).update_or_create(defaults=defaults, **kwargs)
        post_update_or_create.send(sender=self.model, queryset=self, defaults=defaults, **kwargs)
        return return_val

    def delete(self):
        pre_delete.send(sender=self.model, queryset=self)
        return_val = super(SignalQuerySet, self).delete()
        post_delete.send(sender=self.model, queryset=self)
        return return_val

    def update(self, **kwargs):
        pre_update.send(sender=self.model, queryset=self, **kwargs)
        return_val = super(SignalQuerySet, self).update(**kwargs)
        post_update.send(sender=self.model, queryset=self, **kwargs)
        return return_val

    def create(self, **kwargs):
        pre_create.send(sender=self.model, queryset=self, **kwargs)
        return_val = super(SignalQuerySet, self).create(**kwargs)
        post_create.send(sender=self.model, queryset=self, **kwargs)
        return return_val


def monkey_patch_queryset():
    """Monkey patch queryset, thus affecting all querysets."""
    methods = {
        'bulk_create': _bulk_create,
        'get_or_create': _get_or_create,
        'update_or_create': _update_or_create,
        'delete': _delete,
        'update': _update,
        'create': _create,
    }
    for method in methods:
        if hasattr(QuerySet, 'raw_' + method) == False:
            setattr(QuerySet, 'raw_' + method, getattr(QuerySet, method))
            setattr(QuerySet, method, methods[method])


def unpatch_queryset():
    """Un-monkey patch querysets, thus returning all querysets to normal.

    Note:
        There may be caching, and such which delays this operation from taking effect.
    """
    methods = ['bulk_create', 'get_or_create', 'update_or_create', 'delete', 'update', 'create']
    for method in methods:
        try:
            setattr(QuerySet, method, getattr(QuerySet, 'raw_' + method))
            delattr(QuerySet, 'raw_' + method)
        except AttributeError:
            pass
