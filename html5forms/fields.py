from django import forms
from widgets import Html5TextInput, Html5PasswordInput
from widgets import Html5SearchInput, Html5EmailInput
from django.core import validators
from django.utils.encoding import smart_unicode
from django.utils.translation import ugettext_lazy as _

__all__ = (
        'Html5Field', 'Html5CharField', 'Html5PasswordField',
        'Html5SearchField', 'Html5EmailField',
        )


class Html5Field(forms.fields.Field):
    """Base class for Html5 Fields

    Used only for extending
    """

    def __init__(self, placeholder=None, autofocus=False, *args, **kwargs):
        """
        :param placeholder: placeholder text to display if field in unfocused
        :type placeholder: unicode string
        :param autofocus: should the field be focused on load
        :type autofocus: bool
        """

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
    """Your basic inputfield

    :param datalist: a choices list for HTML5 autocomplete feature
    :type datalist: list of tuples

    """
    widget = Html5TextInput

    def __init__(self, max_length=None, min_length=None,
            datalist=None, *args, **kwargs):
        """
        :param datalist: choices for inbuild HTML5 autocompleter
        :type datalist: list of tuples
        :param min_length: minimum length for field
        :type min_length: integer
        :param max_length: maximum length for field
        :type max_length: integer
        """

        self.max_length, self.min_length, self.datalist = max_length,\
                min_length, datalist
        self.widget.datalist = datalist
        super(Html5CharField, self).__init__(*args, **kwargs)
        if min_length is not None:
            self.validators.append(validators.MinLengthValidator(min_length))
        if max_length is not None:
            self.validators.append(validators.MaxLengthValidator(max_length))

    def to_python(self, value):
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


class Html5EmailField(Html5CharField):
    widget = Html5EmailInput
    default_error_messages = {
        'invalid': _(u'Enter a valid e-mail address.'),
    }
    default_validators = [validators.validate_email]
