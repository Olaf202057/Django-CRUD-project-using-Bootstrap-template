from django import forms
from django.contrib.auth import get_user_model, password_validation
from django.core import exceptions

from myproject.common import enums
from myproject.common.forms.baseform import BaseForm

__author__ = "Alex Laird"
__copyright__ = "Copyright 2018, Alex Laird"
__version__ = "0.2.0"


class UserRegisterForm(forms.ModelForm, BaseForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)

    password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput)

    time_zone = forms.ChoiceField(label='Time zone', choices=enums.TIME_ZONE_CHOICES)

    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'time_zone']

    def clean(self):
        """
        Validate attributes, including password constraints, before persisting the user to the database.
        """
        super(UserRegisterForm, self).clean()

        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        if password1 != password2:
            raise forms.ValidationError("You must enter matching passwords.")

        try:
            password_validation.validate_password(password=password1, user=get_user_model())
        except exceptions.ValidationError as e:
            raise forms.ValidationError(list(e.messages))

    def save(self, commit=True):
        """
        Save the provided password in hashed format.

        :param commit: If True, changes to the instance will be saved to the database.
        """
        user = super(UserRegisterForm, self).save(commit=False)
        user.set_password(self.cleaned_data.get("password1"))

        if commit:
            user.save()

        return user
