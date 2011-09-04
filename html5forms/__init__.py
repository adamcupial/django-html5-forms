# -*- coding: utf-8 -*-

from django import forms

class Form(forms.Form):
    """ Same django.form.Form but with jquery validator
    friendly errors output. """

    @property
    def jq_errors(self):
        errors_object = {}
        for key, value in self.errors.iteritems():
            if isinstance(value, (list,tuple)) and len(value) > 0:
                errors_object[key] = value[0]
        return errors_object
