from django import forms

__author__ = "Alex Laird"
__copyright__ = "Copyright 2018, Alex Laird"
__version__ = "0.2.0"


class BaseForm(forms.BaseForm):
    """
    The abstract form from which most other form should inherit to ensure common form functionality is support.
    """

    def __init__(self, *args, **kwargs):
        super(BaseForm, self).__init__(*args, **kwargs)

        for field in list(self.fields.values()):
            field.widget.attrs['placeholder'] = field.label

    class Meta:
        abstract = True
