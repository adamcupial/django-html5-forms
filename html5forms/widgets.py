from django import forms
from django.utils.safestring import mark_safe
from django.utils.encoding import force_unicode
from util import flatatt, render_datalist


class Html5TextInput(forms.widgets.TextInput):

    def render(self, name, value, attrs=None):
        if value is None:
            value = ''
        final_attrs = self.build_attrs(attrs, type=self.input_type, name=name)

        if value != '':
            # Only add the 'value' attribute if a value is non-empty.
            final_attrs['value'] = force_unicode(self._format_value(value))
        if self.datalist is not None\
                and isinstance(self.datalist, (tuple, list)):
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

