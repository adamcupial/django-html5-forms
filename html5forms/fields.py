from django import forms
from widgets import Html5TextInput, Html5PasswordInput, Html5SearchInput
from django.core import validators
from django.utils.encoding import smart_unicode


class Html5Field(forms.fields.Field):

    def __init__(self, placeholder=None, autofocus=False, *args, **kwargs):
        self.placeholder = placeholder
        self.autofocus = autofocus
        super(Html5Field, self).__init__(*args, **kwargs)

    def widget_attrs(self, widget):
        widget_attrs = {}

        if self.placeholder:
            widget_attrs['placeholder'] = self.placeholder

        if self.autofocus:
            widget_attrs['autofocus'] = None

        if self.required:
            widget_attrs['required'] = None
        return widget_attrs

class Html5CharField(Html5Field):
    widget = Html5TextInput

    def __init__(self, max_length=None, min_length=None,
            datalist=None, *args, **kwargs):
        self.max_length, self.min_length, self.datalist = max_length,\
                min_length, datalist
        self.widget.datalist = datalist
        super(Html5CharField, self).__init__(*args, **kwargs)
        if min_length is not None:
            self.validators.append(validators.MinLengthValidator(min_length))
        if max_length is not None:
            self.validators.append(validators.MaxLengthValidator(max_length))

    def to_python(self, value):
        "Returns a Unicode object."
        if value in validators.EMPTY_VALUES:
            return u''
        return smart_unicode(value)

    def widget_attrs(self, widget):
        par_attrs = super(Html5CharField, self).widget_attrs(widget)
        if self.max_length is not None \
                and isinstance(widget, (Html5TextInput, Html5PasswordInput)):
            # The HTML attribute is maxlength, not max_length.
            par_attrs.update({'maxlength': str(self.max_length)})
        return par_attrs

class Html5PasswordField(Html5CharField):
    widget = Html5PasswordInput


class Html5SearchField(Html5CharField):
    widget = Html5SearchInput
