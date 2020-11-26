from django.contrib.auth import get_user_model

__author__ = "Alex Laird"
__copyright__ = "Copyright 2018, Alex Laird"
__version__ = "0.2.0"


def given_a_user_exists(username='test_user', email='user@test.com', password='test_pass_1!'):
    user = get_user_model().objects.create_user(username=username,
                                                email=email,
                                                password=password)

    return user


def given_a_user_exists_and_is_logged_in(client, username='test_user', email='user@test.com',
                                         password='test_pass_1!'):
    user = given_a_user_exists(username, email, password)

    client.login(username=user.get_username(), password=password)

    return user


def verify_user_not_logged_in(test_case):
    test_case.assertNotIn('_auth_user_id', test_case.client.session)


def verify_user_logged_in(test_case):
    test_case.assertIn('_auth_user_id', test_case.client.session)
