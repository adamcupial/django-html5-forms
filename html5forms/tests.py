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


class TestCharField(TestCase):
    def setUp(self):
        class TestForm(Form):
            field = Html5CharField(max_length=20, required=True, class_attr=['test-class'], \
                placeholder='testph', autofocus=True)
        self.form_class = TestForm


    def test_length(self):
        form = self.form_class({'field':'*'*20})
        self.assertTrue(form.is_valid())
    
    def test_length2(self):
        form = self.form_class({'field':'*'*21})
        self.assertFalse(form.is_valid())

    def test_html_output(self):
        form = self.form_class({'field':'**'})
        self.assertIn('maxlength="20"', unicode(form['field']))
        self.assertIn('autofocus', unicode(form['field']))
        self.assertIn(' required ', unicode(form['field']))
        self.assertIn('class="required test-class"', unicode(form['field']))


class TestIntegerField(TestCase):
    def setUp(self):
        class TestForm(Form):
            field = Html5IntegerField(max_value=100, min_value=10)

        self.form_class = TestForm

    def test_min_value(self):
        form = self.form_class({'field': '4'})
        self.assertFalse(form.is_valid())

    def test_min_value2(self):
        form = self.form_class({'field': '11'})
        self.assertTrue(form.is_valid())

    def test_max_value(self):
        form = self.form_class({'field': '101'})
        self.assertFalse(form.is_valid())

    def test_max_value2(self):
        form = self.form_class({'field': '99'})
        self.assertTrue(form.is_valid())

    def test_invalid(self):
        form = self.form_class({'field': '2s'})
        self.assertFalse(form.is_valid())
