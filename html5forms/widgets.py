from django import forms
from django.utils.safestring import mark_safe
from django.utils.encoding import force_unicode
from util import flatatt, render_datalist
from django.utils.html import conditional_escape


class Html5Textarea(forms.widgets.Textarea):

    def __init__(self, attrs=None):
        if attrs is None:
            attrs = {}
        super(Html5Textarea, self).__init__(attrs)


    def render(self, name, value, attrs=None):
        if value is None:
            value = ''
        final_attrs = self.build_attrs(attrs, name=name)

        return mark_safe(u'<textarea%s>%s</textarea>' % (flatatt(final_attrs),
                conditional_escape(force_unicode(value))))


class Html5TextInput(forms.widgets.TextInput):

    def render(self, name, value, attrs=None):
        if value is None:
            value = ''
        final_attrs = self.build_attrs(attrs, type=self.input_type, name=name)

        if value != '':
            # Only add the 'value' attribute if a value is non-empty.
            final_attrs['value'] = force_unicode(self._format_value(value))
        if self.datalist is not None and isinstance(self.datalist, (tuple, list)):
            datalist_name = u'%s_datalist' % name
            final_attrs['list'] = force_unicode(u'%s_datalist' % name)
            return mark_safe(u"""<input%s >%s"""
                    % (flatatt(final_attrs),
                        render_datalist(datalist_name, self.datalist)))
        else:
            return mark_safe(u'<input%s >' % flatatt(final_attrs))



class Html5PasswordInput(Html5TextInput):
    input_type = 'password'

    def __init__(self, *args, **kwargs):
        super(Html5PasswordInput, self).__init__(*args, **kwargs)
        self.datalist = None

class Html5CheckboxInput(forms.widgets.CheckboxInput):
    input_type = 'checkbox'

    def render(self, name, value, attrs=None):
        final_attrs = self.build_attrs(attrs, type='checkbox', name=name)
        try:
            result = self.check_test(value)
        except: # Silently catch exceptions
            result = False
        if result:
            final_attrs['checked'] = 'checked'
        if value not in ('', True, False, None):
            # Only add the 'value' attribute if a value is non-empty.
            final_attrs['value'] = force_unicode(value)
        return mark_safe(u'<input%s />' % flatatt(final_attrs))


class Html5SearchInput(Html5TextInput):
    input_type = 'search'

class Html5EmailInput(Html5TextInput):
    input_type = 'email'

    def __init__(self, *args, **kwargs):
        super(Html5EmailInput, self).__init__(*args, **kwargs)
        self.datalist = None

class Html5URLInput(Html5TextInput):
    input_type = 'url'

class Html5NumberInput(Html5TextInput):
    input_type = 'number'

class Html5RangeInput(Html5NumberInput):
    input_type = 'range'

class Html5TelInput(Html5TextInput):
    input_type = 'tel'
