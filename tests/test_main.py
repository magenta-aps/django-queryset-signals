"The main test module."
from django.test import (
    TestCase,
    override_settings
)
from django.contrib.auth.models import User
from django.db.models.signals import (
    pre_save, post_save,
    pre_delete, post_delete
)

# TODO: Deal with delete signal handler name crash
from django_query_signals import (
    receiver,
    monkey_patch_queryset, unpatch_queryset,
    pre_bulk_create, post_bulk_create,
    pre_delete as qs_pre_delete, post_delete as qs_post_delete,
    pre_get_or_create, post_get_or_create,
    pre_update_or_create, post_update_or_create,
    pre_update, post_update,
)
# TODO: Consider pre_init / post_init
# TODO: Consider m2m_changed


from parameterized import parameterized, parameterized_class


# pylint: disable=unused-variable, unused-argument
class MainTest(TestCase):
    """Test that signal methods are actually called."""

    def setUp(self):
        monkey_patch_queryset()
        # unpatch_queryset()

    def bulk_create_users(self):
        User.objects.bulk_create([
            User(username='test1'),
            User(username='test2')
        ])

    def test_bulk_create(self):
        """Ensure that bulk_create triggers pre_bulk_create signal."""
        tmp = {'pre': False,
               'post': False}

        @receiver(pre_bulk_create)
        def _set_pre(signal, sender, args):
            self.assertEqual(sender, User)
            tmp['pre'] = True

        @receiver(post_bulk_create)
        def _set_post(signal, sender, args):
            self.assertEqual(sender, User)
            tmp['post'] = True

        self.bulk_create_users()

        self.assertTrue(tmp['pre'], msg='pre_bulk_create not called')
        self.assertTrue(tmp['post'], msg='post_bulk_create not called')

    def test_bulk_create_save(self):
        """Check that bulk_create does not trigger pre_save signal."""
        tmp = {'pre': False,
               'post': False}

        @receiver(pre_save)
        def _set_pre(sender, instance, *args, **kwargs):
            self.assertEqual(sender, User)
            tmp['pre'] = True

        @receiver(post_save)
        def _set_post(sender, instance, *args, **kwargs):
            self.assertEqual(sender, User)
            tmp['post'] = True

        self.bulk_create_users()

        self.assertFalse(tmp['pre'], msg='pre_save was called')
        self.assertFalse(tmp['post'], msg='post_save was called')

    @parameterized.expand([
        [True, True, True],
        [False, True, True],
    ])
    def test_delete(self, bulk_create, pre_ok, post_ok):
        """Ensure that queryset delete triggers qs_pre_delete signal."""
        if bulk_create:
            self.bulk_create_users()

        tmp = {'pre': False,
               'post': False}

        @receiver(qs_pre_delete)
        def _set_pre(signal, sender, args):
            self.assertEqual(sender, User)
            tmp['pre'] = True

        @receiver(qs_post_delete)
        def _set_post(signal, sender, args):
            self.assertEqual(sender, User)
            tmp['post'] = True

        users = User.objects.all()
        users.delete()

        self.assertEqual(tmp['pre'], pre_ok, msg='qs_pre_delete not called')
        self.assertEqual(tmp['post'], post_ok, msg='qs_post_delete not called')

    @parameterized.expand([
        [True, True, True],
        [False, False, False],
    ])
    def test_delete_delete(self, bulk_create, pre_ok, post_ok):
        """Ensure that queryset delete triggers pre_delete signal."""
        if bulk_create:
            self.bulk_create_users()

        tmp = {'pre': False,
               'post': False}

        @receiver(pre_delete)
        def _set_pre(sender, instance, *args, **kwargs):
            self.assertEqual(sender, User)
            tmp['pre'] = True

        @receiver(post_delete)
        def _set_post(sender, instance, *args, **kwargs):
            self.assertEqual(sender, User)
            tmp['post'] = True

        users = User.objects.all()
        users.delete()

        self.assertEqual(tmp['pre'], pre_ok, msg='pre_delete not called')
        self.assertEqual(tmp['post'], post_ok, msg='post_delete not called')

    @parameterized.expand([
        [True, True, True],
        [False, True, True],
    ])
    def test_get_or_create(self, precreate, pre_ok, post_ok):
        """Ensure that get_or_create triggers pre_get_or_create signal."""
        if precreate:
            User.objects.create(username='test')

        tmp = {'pre': False,
               'post': False}

        @receiver(pre_get_or_create)
        def _set_pre(signal, sender, args):
            self.assertEqual(sender, User)
            tmp['pre'] = True

        @receiver(post_get_or_create)
        def _set_post(signal, sender, args):
            self.assertEqual(sender, User)
            tmp['post'] = True

        users = User.objects.get_or_create(username='test')

        self.assertEqual(tmp['pre'], pre_ok, msg='pre_get_or_create not called')
        self.assertEqual(tmp['post'], post_ok, msg='post_get_or_create not called')

    @parameterized.expand([
        [True, False, False],
        [False, True, True],
    ])
    def test_get_or_create_save(self, precreate, pre_ok, post_ok):
        """Ensure that get_or_create triggers pre_save signal."""
        if precreate:
            User.objects.create(username='test')

        tmp = {'pre': False,
               'post': False}

        @receiver(pre_save)
        def _set_pre(sender, instance, *args, **kwargs):
            self.assertEqual(sender, User)
            tmp['pre'] = True

        @receiver(post_save)
        def _set_post(sender, instance, *args, **kwargs):
            self.assertEqual(sender, User)
            tmp['post'] = True

        users = User.objects.get_or_create(username='test')

        self.assertEqual(tmp['pre'], pre_ok, msg='pre_save not called')
        self.assertEqual(tmp['post'], post_ok, msg='post_save not called')

    @parameterized.expand([
        [True, True, True],
        [False, True, True],
    ])
    def test_update_or_create(self, precreate, pre_ok, post_ok):
        """Ensure that update_or_create triggers pre_update_or_create signal."""
        if precreate:
            User.objects.create(username='test')

        tmp = {'pre': False,
               'post': False}

        @receiver(pre_update_or_create)
        def _set_pre(signal, sender, args):
            self.assertEqual(sender, User)
            tmp['pre'] = True

        @receiver(post_update_or_create)
        def _set_post(signal, sender, args):
            self.assertEqual(sender, User)
            tmp['post'] = True

        users = User.objects.update_or_create(username='test')

        self.assertEqual(tmp['pre'], pre_ok, msg='pre_update_or_create not called')
        self.assertEqual(tmp['post'], post_ok, msg='post_update_or_create not called')

    @parameterized.expand([
        [True, True, True],
        [False, True, True],
    ])
    def test_update_or_create_save(self, precreate, pre_ok, post_ok):
        """Ensure that update_or_create triggers pre_save signal."""
        if precreate:
            User.objects.create(username='test')

        tmp = {'pre': False,
               'post': False}

        @receiver(pre_save)
        def _set_pre(sender, instance, *args, **kwargs):
            self.assertEqual(sender, User)
            tmp['pre'] = True

        @receiver(post_save)
        def _set_post(sender, instance, *args, **kwargs):
            self.assertEqual(sender, User)
            tmp['post'] = True

        users = User.objects.update_or_create(username='test')

        self.assertEqual(tmp['pre'], pre_ok, msg='pre_save not called')
        self.assertEqual(tmp['post'], post_ok, msg='post_save not called')

    @parameterized.expand([
        [True, True, True],
        [False, True, True],
    ])
    def test_update(self, bulk_create, pre_ok, post_ok):
        """Ensure that queryset update triggers pre_update signal."""
        if bulk_create:
            self.bulk_create_users()

        tmp = {'pre': False,
               'post': False}

        @receiver(pre_update)
        def _set_pre(signal, sender, args):
            self.assertEqual(sender, User)
            tmp['pre'] = True

        @receiver(post_update)
        def _set_post(signal, sender, args):
            self.assertEqual(sender, User)
            tmp['post'] = True

        users = User.objects.all()
        users.update(last_name='Erone')

        self.assertEqual(tmp['pre'], pre_ok, msg='pre_update not called')
        self.assertEqual(tmp['post'], post_ok, msg='post_update not called')

    @parameterized.expand([
        [True, False, False],
        [False, False, False],
    ])
    def test_update_save(self, bulk_create, pre_ok, post_ok):
        """Ensure that queryset update triggers pre_save signal."""
        if bulk_create:
            self.bulk_create_users()

        tmp = {'pre': False,
               'post': False}

        @receiver(pre_save)
        def _set_pre(sender, instance, *args, **kwargs):
            self.assertEqual(sender, User)
            tmp['pre'] = True

        @receiver(post_save)
        def _set_pre(sender, instance, *args, **kwargs):
            self.assertEqual(sender, User)
            tmp['post'] = True

        users = User.objects.all()
        users.update(last_name='Erone')

        self.assertEqual(tmp['pre'], pre_ok, msg='pre_save was called')
        self.assertEqual(tmp['post'], post_ok, msg='post_save was called')
