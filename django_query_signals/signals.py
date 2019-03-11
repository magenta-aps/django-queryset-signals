"""
This module is imported on app ready (see __init__).
"""

from django.db.models.query import QuerySet
from django.dispatch import Signal
from django.conf import settings

# pylint: disable=invalid-name
pre_delete = Signal(providing_args=["args"])
post_delete = Signal(providing_args=["args"])
pre_update = Signal(providing_args=["args"])
post_update = Signal(providing_args=["args"])
pre_bulk_create = Signal(providing_args=["args"])
post_bulk_create = Signal(providing_args=["args"])
pre_get_or_create = Signal(providing_args=["args"])
post_get_or_create = Signal(providing_args=["args"])
pre_update_or_create = Signal(providing_args=["args"])
post_update_or_create = Signal(providing_args=["args"])

METHODS = {'bulk_create':QuerySet.bulk_create,
           'get_or_create':QuerySet.get_or_create,
           'update_or_create':QuerySet.update_or_create,
           'delete':QuerySet.delete,
           'update':QuerySet.update}

def _bulk_create(self, objs, batch_size=None):
    _ = {'self':self, 'objs':objs, 'batch_size':batch_size,
         'method':'bulk_create'}
    pre_bulk_create.send(sender=self.model, args=_)
    _['return'] = METHODS['bulk_create'](_['self'], _['objs'], _['batch_size'])
    post_bulk_create.send(sender=self.model, args=_)
    return _['return']

def _get_or_create(self, defaults=None, **kwargs):
    _ = {'self':self, 'defaults':defaults, 'kwargs':kwargs,
         'method':'get_or_create'}
    pre_get_or_create.send(sender=self.model, args=_)
    _['return'] = METHODS['get_or_create'](
                                        _['self'], _['defaults'], **_['kwargs'])
    post_get_or_create.send(sender=self.model, args=_)
    return _['return']

def _update_or_create(self, defaults=None, **kwargs):
    _ = {'self':self, 'defaults':defaults, 'kwargs':kwargs,
         'method':'update_or_create'}
    pre_update_or_create.send(sender=self.model, args=_)
    _['return'] = METHODS['update_or_create'](
                                        _['self'], _['defaults'], **_['kwargs'])
    post_update_or_create.send(sender=self.model, args=_)
    return _['return']

def _delete(self):
    _ = {'self':self, 'method':'delete'}
    pre_delete.send(sender=self.model, args=_)
    _['return'] = METHODS['delete'](_['self'])
    post_delete.send(sender=self.model, args=_)
    return _['return']

def _update(self, **kwargs):
    _ = {'self':self, 'kwargs':kwargs, 'method':'update'}
    pre_update.send(sender=self.model, args=_)
    _['return'] = METHODS['update'](_['self'], **_['kwargs'])
    post_update.send(sender=self.model, args=_)
    return _['return']


class SignalQuerySet(QuerySet):
    # https://docs.djangoproject.com/en/1.11/_modules/django/db/models/query/#QuerySet
    def bulk_create(self, objs, batch_size=None):
        return _bulk_create(self, objs, batch_size)

    def delete(self):
        return _delete(self)

    def update(self, **kwargs):
        return _update(**kwargs)


def monkey_patch_queryset():
    QuerySet.old_bulk_create = QuerySet.bulk_create
    QuerySet.bulk_create = _bulk_create

    QuerySet.old_get_or_create = QuerySet.get_or_create
    QuerySet.get_or_create = _get_or_create

    QuerySet.old_update_or_create = QuerySet.update_or_create
    QuerySet.update_or_create = _update_or_create

    QuerySet.old_delete = QuerySet.delete
    QuerySet.delete = _delete

    QuerySet.old_update = QuerySet.update
    QuerySet.update = _update


def unpatch_queryset():
    methods = ['bulk_create', 'get_or_create', 'update_or_create', 'delete', 'update']
    for method in methods:
        try:
            setattr(QuerySet, method, getattr(QuerySet, 'old_' + method))
        except AttributeError:
            pass
