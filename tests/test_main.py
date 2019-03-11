"The main test module."
from django.test import TestCase
from django.contrib.auth.models import User
from django.db.models.signals import (
    pre_save, post_save,
    pre_delete, post_delete
)

# TODO: Deal with delete signal handler name crash
from django_query_signals import (
    receiver,
    pre_bulk_create, post_bulk_create,
    pre_delete as qs_pre_delete, post_delete as qs_post_delete,
    pre_get_or_create, post_get_or_create,
    pre_update_or_create, post_update_or_create,
    pre_update, post_update,
)
# TODO: Consider pre_init / post_init
# TODO: Consider m2m_changed


# pylint: disable=unused-variable, unused-argument
class MainTest(TestCase):
    """Test that signal methods are actually called."""

    def test_01_bulk_create(self):
        """Ensure that bulk_create triggers pre_bulk_create signal."""
        tmp = {'pre':False,
               'post':False}

        @receiver(pre_bulk_create)
        def _set_pre(signal, sender, args):
            self.assertEqual(sender, User)
            tmp['pre'] = True

        @receiver(post_bulk_create)
        def _set_post(signal, sender, args):
            self.assertEqual(sender, User)
            tmp['post'] = True

        User.objects.bulk_create([User(username='test1'),
                                  User(username='test2')])

        self.assertTrue(tmp['pre'], msg='pre_bulk_create not called')
        self.assertTrue(tmp['post'], msg='post_bulk_create not called')

    def test_01_bulk_create_save(self):
        """Check that bulk_create does not trigger pre_save signal."""
        tmp = {'pre':False,
               'post':False}

        @receiver(pre_save)
        def _set_pre(sender, instance, *args, **kwargs):
            self.assertEqual(sender, User)
            tmp['pre'] = True

        @receiver(post_save)
        def _set_post(sender, instance, *args, **kwargs):
            self.assertEqual(sender, User)
            tmp['post'] = True

        User.objects.bulk_create([User(username='test1'),
                                  User(username='test2')])

        self.assertFalse(tmp['pre'], msg='pre_save was called')
        self.assertFalse(tmp['post'], msg='post_save was called')

    def test_02_delete(self):
        """Ensure that queryset delete triggers qs_pre_delete signal."""
        tmp = {'pre':False,
               'post':False}

        @receiver(qs_pre_delete)
        def _set_pre(signal, sender, args):
            self.assertEqual(sender, User)
            tmp['pre'] = True

        @receiver(qs_post_delete)
        def _set_post(signal, sender, args):
            self.assertEqual(sender, User)
            tmp['post'] = True

        self.test_01_bulk_create()
        users = User.objects.all()
        users.delete()

        self.assertTrue(tmp['pre'], msg='qs_pre_delete not called')
        self.assertTrue(tmp['post'], msg='qs_post_delete not called')

    def test_02_delete_delete(self):
        """Ensure that queryset delete triggers pre_delete signal."""
        tmp = {'pre':False,
               'post':False}

        @receiver(pre_delete)
        def _set_pre(sender, instance, *args, **kwargs):
            self.assertEqual(sender, User)
            tmp['pre'] = True

        @receiver(post_delete)
        def _set_post(sender, instance, *args, **kwargs):
            self.assertEqual(sender, User)
            tmp['post'] = True

        self.test_01_bulk_create()
        users = User.objects.all()
        users.delete()

        self.assertTrue(tmp['pre'], msg='pre_delete not called')
        self.assertTrue(tmp['post'], msg='post_delete not called')

    # TODO: Test get part of get_or_create
    def test_03_get_or_create(self):
        """Ensure that get_or_create triggers pre_get_or_create signal."""
        tmp = {'pre':False,
               'post':False}

        @receiver(pre_get_or_create)
        def _set_pre(signal, sender, args):
            self.assertEqual(sender, User)
            tmp['pre'] = True

        @receiver(post_get_or_create)
        def _set_post(signal, sender, args):
            self.assertEqual(sender, User)
            tmp['post'] = True

        users = User.objects.get_or_create(username='test')

        self.assertTrue(tmp['pre'], msg='pre_get_or_create not called')
        self.assertTrue(tmp['post'], msg='post_get_or_create not called')

    # TODO: Test get part of get_or_create
    def test_03_get_or_create_save(self):
        """Ensure that get_or_create triggers pre_save signal."""
        tmp = {'pre':False,
               'post':False}

        @receiver(pre_save)
        def _set_pre(sender, instance, *args, **kwargs):
            self.assertEqual(sender, User)
            tmp['pre'] = True

        @receiver(post_save)
        def _set_post(sender, instance, *args, **kwargs):
            self.assertEqual(sender, User)
            tmp['post'] = True

        users = User.objects.get_or_create(username='test')

        self.assertTrue(tmp['pre'], msg='pre_save not called')
        self.assertTrue(tmp['post'], msg='post_save not called')

    # TODO: Test update part of update_or_create
    def test_04_update_or_create(self):
        """Ensure that update_or_create triggers pre_update_or_create signal."""
        tmp = {'pre':False,
               'post':False}

        @receiver(pre_update_or_create)
        def _set_pre(signal, sender, args):
            self.assertEqual(sender, User)
            tmp['pre'] = True

        @receiver(post_update_or_create)
        def _set_post(signal, sender, args):
            self.assertEqual(sender, User)
            tmp['post'] = True

        users = User.objects.update_or_create(username='test')

        self.assertTrue(tmp['pre'], msg='pre_update_or_create not called')
        self.assertTrue(tmp['post'], msg='post_update_or_create not called')

    # TODO: Test update part of update_or_create
    def test_04_update_or_create_save(self):
        """Ensure that update_or_create triggers pre_save signal."""
        tmp = {'pre':False,
               'post':False}

        @receiver(pre_save)
        def _set_pre(sender, instance, *args, **kwargs):
            self.assertEqual(sender, User)
            tmp['pre'] = True

        @receiver(post_save)
        def _set_post(sender, instance, *args, **kwargs):
            self.assertEqual(sender, User)
            tmp['post'] = True

        users = User.objects.update_or_create(username='test')

        self.assertTrue(tmp['pre'], msg='pre_save not called')
        self.assertTrue(tmp['post'], msg='post_save not called')

    def test_05_update(self):
        """Ensure that queryset update triggers pre_update signal."""
        tmp = {'pre':False,
               'post':False}

        @receiver(pre_update)
        def _set_pre(signal, sender, args):
            self.assertEqual(sender, User)
            tmp['pre'] = True

        @receiver(post_update)
        def _set_post(signal, sender, args):
            self.assertEqual(sender, User)
            tmp['post'] = True

        self.test_01_bulk_create()
        users = User.objects.all()
        users.update(last_name='Erone')

        self.assertTrue(tmp['pre'], msg='pre_update not called')
        self.assertTrue(tmp['post'], msg='post_update not called')

    def test_05_update_save(self):
        """Ensure that queryset update triggers pre_save signal."""
        tmp = {'pre':False,
               'post':False}

        @receiver(pre_save)
        def _set_pre(sender, instance, *args, **kwargs):
            self.assertEqual(sender, User)
            tmp['pre'] = True

        @receiver(post_save)
        def _set_pre(sender, instance, *args, **kwargs):
            self.assertEqual(sender, User)
            tmp['post'] = True

        self.test_01_bulk_create()
        users = User.objects.all()
        users.update(last_name='Erone')

        self.assertFalse(tmp['pre'], msg='pre_save was called')
        self.assertFalse(tmp['post'], msg='post_save was called')
