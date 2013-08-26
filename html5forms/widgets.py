from django import forms
from django.utils.safestring import mark_safe
from django.utils.encoding import force_unicode, force_text
from django.utils.html import format_html
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
        if getattr(self, 'datalist', None) and isinstance(self.datalist, (tuple, list)):
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


class Html5Select(forms.Select):

    def render_option(self, selected_choices, option_value, option_label, *args, **kw):
        option_value = force_text(option_value)
        selected_html = ''
        if args and type(args[0]) == type({}):
            selected_html += flatatt(args[0])
        if option_value in selected_choices:
            selected_html += ' selected="selected"'
            if not self.allow_multiple_selected:
                # Only allow for a single selection.
                selected_choices.remove(option_value)
        selected_html = mark_safe(selected_html)
        return format_html(u'<option value="{0}"{1}>{2}</option>',
                option_value, selected_html, force_unicode(option_label))

class Html5TelInput(Html5TextInput):
    input_type = 'tel'
