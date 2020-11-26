from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from myproject.auth.tests.helpers import userhelper

__author__ = "Alex Laird"
__copyright__ = "Copyright 2018, Alex Laird"
__version__ = "0.2.0"


class TestCaseAuthViews(TestCase):
    def test_settings_view(self):
        # GIVEN
        userhelper.given_a_user_exists_and_is_logged_in(self.client)

        # WHEN
        response = self.client.get(reverse('settings'))

        # THEN
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'settings.html')

    def test_password_reset(self):
        # GIVEN
        user = userhelper.given_a_user_exists()
        response = self.client.post(reverse('forgot'), {'email': user.email})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('login'))
        temp_pass = response.context['password']

        # WHEN
        response = self.client.post(reverse('login'), {'username': user.get_username(), 'password': temp_pass})

        # THEN
        self.assertEqual(response.status_code, 302)
        userhelper.verify_user_logged_in(self)

    def test_password_reset_real_fake_user_same_response(self):
        # GIVEN
        user = userhelper.given_a_user_exists()

        # WHEN
        response1 = self.client.post(reverse('forgot'), {'email': user.email})
        status1 = response1.cookies['status_msg'].value
        response2 = self.client.post(reverse('forgot'), {'email': 'fake@fake.com'})
        status2 = response2.cookies['status_msg'].value

        # WHEN
        self.assertIn('been emailed a temporary password', status1)
        self.assertEqual(status1, status2)

    def test_registration_success(self):
        # GIVEN
        userhelper.verify_user_not_logged_in(self)

        # WHEN
        response = self.client.post(reverse('register'),
                                    {'email': 'test@test.com', 'username': 'my_test_user', 'password1': 'test_pass_1!',
                                     'password2': 'test_pass_1!', 'time_zone': 'America/Chicago'})

        # THEN
        userhelper.verify_user_not_logged_in(self)
        user = get_user_model().objects.get(email='test@test.com')
        self.assertEqual(user.username, 'my_test_user')
        self.assertEqual(user.time_zone, 'America/Chicago')
        self.assertIn('good to go', self.client.cookies['status_msg'].value)
        self.assertRedirects(response, reverse('login'))

    def test_registration_bad_data(self):
        # GIVEN
        userhelper.verify_user_not_logged_in(self)

        # WHEN
        response = self.client.post(reverse('register'),
                                    {'email': 'test@not-a-valid-email', 'username': 'my_test_user',
                                     'password1': 'test_pass_1!', 'password2': 'test_pass_1!',
                                     'time_zone': 'America/Chicago'})

        # THEN
        userhelper.verify_user_not_logged_in(self)
        self.assertFalse(get_user_model().objects.filter(username='my_test_user').exists())
        self.assertContains(response, 'valid email address')

    def test_registration_password_insufficient(self):
        # GIVEN
        userhelper.verify_user_not_logged_in(self)

        # WHEN
        response = self.client.post(reverse('register'),
                                    {'email': 'test@test.com', 'username': 'my_test_user',
                                     'password1': 'short', 'password2': 'short',
                                     'time_zone': 'America/Chicago'})

        # THEN
        userhelper.verify_user_not_logged_in(self)
        self.assertFalse(get_user_model().objects.filter(username='my_test_user').exists())
        self.assertContains(response, 'password is too short')

    def test_registration_password_mismatch(self):
        # GIVEN
        userhelper.verify_user_not_logged_in(self)

        # WHEN
        response = self.client.post(reverse('register'),
                                    {'email': 'test@test.com', 'username': 'my_test_user',
                                     'password1': 'test_pass_1', 'password2': 'test_pass_2',
                                     'time_zone': 'America/Chicago'})

        # THEN
        userhelper.verify_user_not_logged_in(self)
        self.assertFalse(get_user_model().objects.filter(username='my_test_user').exists())
        self.assertContains(response, 'enter matching passwords')

    def test_login_username_success(self):
        # GIVEN
        user = userhelper.given_a_user_exists()
        userhelper.verify_user_not_logged_in(self)

        # WHEN
        response = self.client.post(reverse('login') + '?next={}'.format(reverse('settings')),
                                    {'username': user.get_username(), 'password': 'test_pass_1!',
                                     'remember-me': 'remember-me'})

        # THEN
        self.assertRedirects(response, reverse('settings'))
        userhelper.verify_user_logged_in(self)

    def test_login_email_success(self):
        # GIVEN
        user = userhelper.given_a_user_exists()
        userhelper.verify_user_not_logged_in(self)

        # WHEN
        response = self.client.post(reverse('login'), {'username': user.email, 'password': 'test_pass_1!'})

        # THEN
        self.assertRedirects(response, reverse('portal'), fetch_redirect_response=False)
        userhelper.verify_user_logged_in(self)

    def test_login_bad_data(self):
        # GIVEN
        user = userhelper.given_a_user_exists()
        userhelper.verify_user_not_logged_in(self)

        # WHEN
        response = self.client.post(reverse('login'), {'username': user.username})

        # THEN
        userhelper.verify_user_not_logged_in(self)
        self.assertContains(response, 'This field is required', status_code=401)

    def test_login_wrong_password(self):
        # GIVEN
        user = userhelper.given_a_user_exists()
        userhelper.verify_user_not_logged_in(self)

        # WHEN
        response = self.client.post(reverse('login'), {'username': user.email, 'password': 'wrong-pass'})

        # THEN
        self.assertContains(response, 'entered your credentials properly', status_code=401)

    def test_logout_success(self):
        # GIVEN
        userhelper.given_a_user_exists_and_is_logged_in(self.client)

        # WHEN
        response = self.client.post(reverse('logout'))

        # THEN
        self.assertEqual(response.status_code, 302)
        userhelper.verify_user_not_logged_in(self)

    def test_authenticated_view_success(self):
        # GIVEN
        user = userhelper.given_a_user_exists(self.client)

        # WHEN
        response1 = self.client.get(reverse('settings'))
        self.client.login(username=user.get_username(), password='test_pass_1!')
        response2 = self.client.get(reverse('settings'))

        # THEN
        self.assertRedirects(response1, reverse('login') + '?next={}'.format(reverse('settings')),
                             fetch_redirect_response=False)
        self.assertEqual(response2.status_code, 200)
