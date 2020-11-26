from django import forms
from django.contrib.auth import admin
from django.contrib.auth import get_user_model
from django.contrib.auth import password_validation
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.core import exceptions

from myproject.common.admin import BaseModelAdmin, admin_site

__author__ = "Alex Laird"
__copyright__ = "Copyright 2018, Alex Laird"
__version__ = "0.2.0"


class AdminUserCreationForm(UserCreationForm):
    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        if password1 != password2:
            raise forms.ValidationError("You must enter matching passwords.")

        try:
            password_validation.validate_password(password=password1, user=get_user_model())
        except exceptions.ValidationError as e:
            raise forms.ValidationError(list(e.messages))

        return password1


class UserAdmin(admin.UserAdmin, BaseModelAdmin):
    form = UserChangeForm
    add_form = AdminUserCreationForm

    list_display = ('email', 'username', 'created_at', 'last_login', 'is_superuser')
    list_filter = ('is_superuser',)
    search_fields = ('email', 'username')
    ordering = ('-last_login',)
    add_fieldsets = (
        (None, {
            'fields': ('username', 'email', 'password1', 'password2',),
        }),
    )
    fieldsets = None
    filter_horizontal = ()

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return self.readonly_fields + ('created_at', 'last_login',)

        return self.readonly_fields


# Register the models in the Admin
admin_site.register(get_user_model(), UserAdmin)
