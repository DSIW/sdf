from django.core.management import call_command
from django.test import TestCase


class ViewTests(TestCase):

    def setUp(self):
        # Load fixtures
        call_command('loaddata', 'fixtures/testuser', verbosity=0)