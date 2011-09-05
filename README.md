Author: Adam Cupiał

Contributors: Andrei Antoukh, Ben Lopatin

# Description

Formfields in django are not suited for HTML5, hence this app

# Installation

 1. clone repository git clone git://github.com/adamcupial/django-html5-forms.git, put it somewhere in your python path
 2. add 'html5forms' to INSTALLED_APPS (not required)
 3. use appropriate form fields in your forms (since the widgets requires some additional attributes passed from forms, you should use fields)

# Fields

## All fields

### Attributes
 * all the core attributes from django field
 * placeholder :text, which displays on the field when it is empty and unfocused
 * autofocus (true/false), automaticaly set focus to element on page load

## Html5CharField

widget: Html5TextInput

### Description
 Typical CharField, most common field in the internet, allows datalist choices, which is great autocomplete feature

### Attributes
 * all the attr of django CharField
 * datalist: list or tuple, of words for autocompletion (sng like autocomplete in firefox or chrome)

## Html5PasswordField

widget: Html5PasswordInput

### Description
 Typical PasswordField, does not allow datalist choices

### Attributes
 * all the attr of django CharField/PasswordField

## Html5SearchField

widget: Html5SearchInput

### Description
  New field in HTML5 - the same as CharField only different input type, should be used in search fields, allows datalists

### Attributes
 * all the attr of django CharField/PasswordField
