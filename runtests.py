#!/usr/bin/env python
# NOTE: Created according to: https://docs.djangoproject.com/en/1.11/topics/testing/advanced/#using-the-django-test-runner-to-test-reusable-applications
import os
import sys

import django
from django.conf import settings
from django.test.utils import get_runner

if __name__ == "__main__":
    # pylint: disable=invalid-name
    argv = sys.argv
    # pylint: disable=invalid-name
    specific_test = argv[1] if len(argv) > 1 else None

    os.environ['DJANGO_SETTINGS_MODULE'] = 'tests.test_settings'
    django.setup()
    TestRunner = get_runner(settings)
    test_runner = TestRunner()
    if specific_test:
        failures = test_runner.run_tests([specific_test])
    else:
        failures = test_runner.run_tests(["tests"])
    sys.exit(bool(failures))
