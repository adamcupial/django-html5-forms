# -*- coding: utf-8 -*-

from django.test import TestCase
from html5forms import Form
from html5forms.fields import *

class TestBooleanField(TestCase):
    def setUp(self):
        class TestForm(Form):
            field = Html5BooleanField(required=False)

        self.form_class = TestForm

    def test_false1(self):
        form = self.form_class({'field':'False'})
        self.assertTrue(form.is_valid())
        self.assertFalse(form.cleaned_data['field'])
    
    def test_false2(self):
        form = self.form_class({'field':'0'})
        self.assertTrue(form.is_valid())
        self.assertFalse(form.cleaned_data['field'])

    def test_true(self):
        form = self.form_class({'field':'t'})
        self.assertTrue(form.is_valid())
        self.assertTrue(form.cleaned_data['field'])

    def test_form(self):
        form = self.form_class({'field':'t'})
        self.assertEqual(unicode(form['field']), 
            '<input checked="checked" type="checkbox" name="field" value="t" id="id_field" />')
