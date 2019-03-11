"""
This module is imported on app ready (see __init__).
"""

from django.db.models.query import QuerySet
from django.dispatch import Signal
from django.conf import settings

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


def monkey_patch_queryset():
    """Monkey patch queryset, thus affecting all querysets."""
    methods = {
        'bulk_create': _bulk_create,
        'get_or_create': _get_or_create,
        'update_or_create': _update_or_create,
        'delete': _delete,
        'update': _update,
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
    methods = ['bulk_create', 'get_or_create', 'update_or_create', 'delete', 'update']
    for method in methods:
        try:
            setattr(QuerySet, method, getattr(QuerySet, 'raw_' + method))
            delattr(QuerySet, 'raw_' + method)
        except AttributeError:
            pass
