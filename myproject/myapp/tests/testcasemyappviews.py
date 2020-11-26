from django.test import TestCase
from django.urls import reverse

from myproject.auth.tests.helpers import userhelper

__author__ = "Alex Laird"
__copyright__ = "Copyright 2018, Alex Laird"
__version__ = "0.2.0"


class TestCaseMyAppViews(TestCase):
    def test_portal_view(self):
        # GIVEN
        userhelper.given_a_user_exists_and_is_logged_in(self.client)

        # WHEN
        response = self.client.get(reverse('portal'))

        # THEN
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'portal.html')
