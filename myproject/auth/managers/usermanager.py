import logging

from django.contrib.auth.models import BaseUserManager
from django.db.models import Q

__author__ = "Alex Laird"
__copyright__ = "Copyright 2018, Alex Laird"
__version__ = "0.2.0"

logger = logging.getLogger(__name__)


class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None):  # pragma: no cover
        """
        Create a new user with the given attributes.

        :param username: the username for the user
        :param email: the email for the new user
        :param password: the password for the new user
        :return: the created object
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            username=username
        )

        user.set_password(password)

        user.save(using=self._db)

        return user

    def create_superuser(self, email, username, password):  # pragma: no cover
        """
        Create a new super user with admin privileges.

        :param username: the username for the user
        :param email: the email for the new user
        :param password: the password for the new user
        :return: the created object
        """
        user = self.create_user(username=username,
                                email=email,
                                password=password)
        user.is_superuser = True
        user.save(using=self._db)
        return user

    def get_by_natural_key(self, username):
        """
        Get the user for authentication/login from the database.

        :param username: the username to lookup
        :return: the user
        """
        return self.get(Q(username__iexact=username) | Q(email__iexact=username))
