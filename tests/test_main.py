"The main test module."
from django.test import (
    TestCase,
    override_settings
)
from django.contrib.auth.models import User
from django.db.models.query import QuerySet
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
class MonkeyPatchTest(TestCase):
    """Test that signal methods are actually called."""

    def setUp(self):
        pass
        # monkey_patch_queryset()
        # unpatch_queryset()

    def test_monkey(self):
        pre_normal_method = QuerySet.bulk_create
        monkey_patch_queryset()
        pre_monkey_method = QuerySet.bulk_create
        unpatch_queryset()
        post_normal_method = QuerySet.bulk_create
        monkey_patch_queryset()
        post_monkey_method = QuerySet.bulk_create
        unpatch_queryset()

        self.assertEqual(pre_normal_method, post_normal_method)
        self.assertEqual(pre_monkey_method, post_monkey_method)
        self.assertNotEqual(pre_monkey_method, pre_normal_method)

    # ---------------- #
    # Helper functions #
    # ---------------- #
    def bulk_create_users(self):
        User.objects.bulk_create([
            User(username='test1'),
            User(username='test2')
        ])

    def delete_users(self):
        users = User.objects.all()
        users.delete()

    def get_or_create_user(self):
        User.objects.get_or_create(username='test')

    def update_or_create_user(self):
        User.objects.update_or_create(username='test')

    def update_users(self):
        users = User.objects.all()
        users.update(last_name='Erone')

    # ----------------- #
    # Testing functions #
    # ----------------- #
    @parameterized.expand([
        # Action = bulk_create_users
        # bulk_create signals triggered
        [bulk_create_users, pre_bulk_create, True],
        [bulk_create_users, post_bulk_create, True],
        # save signals not triggered
        [bulk_create_users, pre_save, False],
        [bulk_create_users, post_save, False],

        # Action = delete_users
        # qs_delete delete signals triggered
        [delete_users, qs_pre_delete, True],
        [delete_users, qs_post_delete, True],
        [delete_users, qs_pre_delete, True, bulk_create_users],
        [delete_users, qs_post_delete, True, bulk_create_users],
        # delete signals triggered depending on data
        # 
        [delete_users, pre_delete, False],
        [delete_users, post_delete, False],
        [delete_users, pre_delete, True, bulk_create_users],
        [delete_users, post_delete, True, bulk_create_users],

        # Action = get_or_create_user
        # get_or_create signals triggered
        [get_or_create_user, pre_get_or_create, True],
        [get_or_create_user, post_get_or_create, True],
        [get_or_create_user, pre_get_or_create, True, get_or_create_user],
        [get_or_create_user, post_get_or_create, True, get_or_create_user],
        # save signals triggered depending on data
        # - only triggered when creating
        [get_or_create_user, pre_save, True],
        [get_or_create_user, post_save, True],
        [get_or_create_user, pre_save, False, get_or_create_user],
        [get_or_create_user, post_save, False, get_or_create_user],

        # Action = update_or_create_user
        # update_or_create signals triggered
        [update_or_create_user, pre_update_or_create, True],
        [update_or_create_user, post_update_or_create, True],
        [update_or_create_user, pre_update_or_create, True, update_or_create_user],
        [update_or_create_user, post_update_or_create, True, update_or_create_user],
        # save signals triggered
        [update_or_create_user, pre_save, True],
        [update_or_create_user, post_save, True],
        [update_or_create_user, pre_save, True, update_or_create_user],
        [update_or_create_user, post_save, True, update_or_create_user],

        # Action = update_users
        # update_or_create signals triggered
        [update_users, pre_update, True],
        [update_users, post_update, True],
        [update_users, pre_update, True, bulk_create_users],
        [update_users, post_update, True, bulk_create_users],
        # save signals triggered
        [update_users, pre_save, False],
        [update_users, post_save, False],
        [update_users, pre_save, False, bulk_create_users],
        [update_users, post_save, False, bulk_create_users],
    ])
    # TODO: Add custom function names aka. testcase_func_name=custom_name_func
    def test_signals(self, trigger, signal, expected, pre_task = None):
        """Ensure that signal behaves as expected."""
        monkey_patch_queryset()

        if pre_task:
            pre_task(self)

        tmp = {'signal': False}

        @receiver(signal)
        def _signal_handler(*args, **kwargs):
            sender = kwargs['sender']
            self.assertEqual(sender, User)
            tmp['signal'] = True

        trigger(self)

        self.assertEqual(tmp['signal'], expected)
