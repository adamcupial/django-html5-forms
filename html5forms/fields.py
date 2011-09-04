from django import forms
from django.utils import formats
from django.core.exceptions import ValidationError
from widgets import Html5TextInput, Html5PasswordInput, Html5CheckboxInput
from widgets import Html5SearchInput, Html5EmailInput
from widgets import Html5URLInput, Html5NumberInput
from django.core import validators, exceptions
from django.utils.encoding import smart_unicode
from django.utils.translation import ugettext_lazy as _
import urlparse


__all__ = (
        'Html5Field', 'Html5CharField', 'Html5PasswordField',
        'Html5SearchField', 'Html5EmailField', 'Html5URLField',
        'Html5IntegerField'
        )


class Html5Field(forms.fields.Field):
    """Base class for Html5 Fields

    Used only for extending

    :param placeholder: placeholder text to display if field in unfocused
    :type placeholder: String
    :param autofocus: should the field be focused on load
    :type autofocus: Boolean
    """

    def __init__(self, placeholder=None, autofocus=False, class_attr=[], *args, **kwargs):
        self.placeholder = placeholder
        self.autofocus = autofocus
        self.class_attr = class_attr
        super(Html5Field, self).__init__(*args, **kwargs)

    def widget_attrs(self, widget):
        widget_attrs = super(CharField, self).widget_attrs(widget)
        current_class = widget_attrs.get('class', '')

        if self.placeholder:
            widget_attrs['placeholder'] = self.placeholder

        if self.autofocus:
            widget_attrs['autofocus'] = None

        if self.required:
            widget_attrs['required'] = None
            current_class.append('required')

        if isinstance(self.class_attr, (str, unicode)):
            self.class_attr = self.class_attr.split()

        for classitem in self.class_attr:
            if classitem not in current_class:
                current_class.append(classitem)

        if current_class:
            widget_attrs['class'] = ' '.join(current_class)

        return widget_attrs

class Html5BooleanField(Html5Field):
    widget = Html5CheckboxInput

    def to_python(self, value):
        """Returns a Python boolean object."""
        # Explicitly check for the string 'False', which is what a hidden field
        # will submit for False. Also check for '0', since this is what
        # RadioSelect will provide. Because bool("True") == bool('1') == True,
        # we don't need to handle that explicitly.
        if value in ('False', '0'):
            value = False
        else:
            value = bool(value)
        value = super(Html5BooleanField, self).to_python(value)
        if not value and self.required:
            raise ValidationError(self.error_messages['required'])
        return value


    def widget_attrs(self, widget):
        widget_attrs = {}

        if self.autofocus:
            widget_attrs['autofocus'] = None

        if self.required:
            widget_attrs['required'] = None

        return widget_attrs


class Html5CharField(Html5Field):
    """Your basic inputfield

    :param placeholder: placeholder text to display if field in unfocused
    :type placeholder: String
    :param autofocus: should the field be focused on load
    :type autofocus: Boolean
    :param datalist: choices for inbuild HTML5 autocompleter
    :type datalist: list of two-tuples
    :param min_length: minimum length for field
    :type min_length: Integer
    :param max_length: maximum length for field
    :type max_length: Integer
    """

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
    """ Password field

    :param placeholder: placeholder text to display if field in unfocused
    :type placeholder: String
    :param autofocus: should the field be focused on load
    :type autofocus: Boolean
    :param min_length: minimum length for field
    :type min_length: Integer
    :param max_length: maximum length for field
    :type max_length: Integer
    """

    widget = Html5PasswordInput


class Html5SearchField(Html5CharField):
    """ Search field

    apart from default widget works just like CharField
    """
    widget = Html5SearchInput


class Html5EmailField(Html5CharField):
    """ Email Field

    :param placeholder: placeholder text to display if field in unfocused
    :type placeholder: String
    :param autofocus: should the field be focused on load
    :type autofocus: Boolean
    :param datalist: choices for inbuild HTML5 autocompleter
    :type datalist: list of two-tuples
    :param min_length: minimum length for field
    :type min_length: Integer
    :param max_length: maximum length for field
    :type max_length: Integer
    """

    widget = Html5EmailInput
    default_error_messages = {
        'invalid': _(u'Enter a valid e-mail address.'),
    }
    default_validators = [validators.validate_email]


class Html5URLField(Html5CharField):
    """ Url Field

    :param placeholder: placeholder text to display if field in unfocused
    :type placeholder: String
    :param autofocus: should the field be focused on load
    :type autofocus: Boolean
    :param datalist: choices for inbuild HTML5 autocompleter
    :type datalist: list of two-tuples
    :param min_length: minimum length for field
    :type min_length: Integer
    :param max_length: maximum length for field
    :type max_length: Integer
    :param verify_exists: check whether specified url address exists (is not 404), default False
    :type verify_exists: Boolean
    :param validator_user_agent: String used as the user-agent used when checking for a URL's existence. Defaults to the value of the URL_VALIDATOR_USER_AGENT setting.
    :type validator_user_agent: String
    """

    widget = Html5URLInput
    default_error_messages = {
        'invalid': _(u'Enter a valid URL.'),
        'invalid_link': _(u'This URL appears to be a broken link.'),
    }

    def __init__(self, max_length=None, min_length=None, verify_exists=False,
            validator_user_agent=validators.URL_VALIDATOR_USER_AGENT, *args, **kwargs):
        super(Html5URLField, self).__init__(max_length, min_length, *args,
                                       **kwargs)
        self.validators.append(validators.URLValidator(verify_exists=verify_exists, validator_user_agent=validator_user_agent))

    def to_python(self, value):
        if value:
            if '://' not in value:
                # If no URL scheme given, assume http://
                value = u'http://%s' % value
            url_fields = list(urlparse.urlsplit(value))
            if not url_fields[2]:
                # the path portion may need to be added before query params
                url_fields[2] = '/'
                value = urlparse.urlunsplit(url_fields)
        return super(Html5URLField, self).to_python(value)


class Html5IntegerField(Html5Field):
    """ Integer Field

    :param placeholder: placeholder text to display if field in unfocused
    :type placeholder: String
    :param autofocus: should the field be focused on load
    :type autofocus: Boolean
    :param min_value: minimum value for field
    :type min_value: Integer
    :param max_value: maximum value for field
    :type max_value: Integer
    :param step: step for number selector (eg. 2 for 2,4,6,8...)
    :type step: Integer
    """

    widget = Html5NumberInput

    default_error_messages = {
        'invalid': _(u'Enter a whole number.'),
        'max_value': _(u'Ensure this value is less than or equal to %(limit_value)s.'),
        'min_value': _(u'Ensure this value is greater than or equal to %(limit_value)s.'),
    }

    def __init__(self, max_value=None, min_value=None, step=None, *args, **kwargs):

        self.max_value = max_value
        self.min_value = min_value
        self.step = step

        super(Html5IntegerField, self).__init__(*args, **kwargs)

        if self.max_value is not None:
            self.validators.append(validators.MaxValueValidator(self.max_value))
        if self.min_value is not None:
            self.validators.append(validators.MinValueValidator(self.min_value))

    def widget_attrs(self, widget):
        par_attrs = super(Html5IntegerField, self).widget_attrs(widget)
        if self.max_value is not None:
            par_attrs.update({'max': str(self.max_value)})
        if self.min_value is not None:
            par_attrs.update({'min': str(self.min_value)})
        if self.step is not None:
            par_attrs.update({'step': str(self.step)})
        return par_attrs

    def to_python(self, value):
        """
        Validates that int() can be called on the input. Returns the result
        of int(). Returns None for empty values.
        """
        value = super(Html5IntegerField, self).to_python(value)
        if value in validators.EMPTY_VALUES:
            return None
        if self.localize:
            value = formats.sanitize_separators(value)
        try:
            value = int(str(value))
        except (ValueError, TypeError):
            raise exceptions.ValidationError(self.error_messages['invalid'])
        return value
