#!/usr/local/bin/python
# coding: utf-8

from setuptools import setup, find_packages

DESCRIPTION = "HTML5 forms for Django."

try:
    LONG_DESCRIPTION = open('README.md').read()
except:
    LONG_DESCRIPTION = DESCRIPTION


setup(name='html5forms',
      version='0.0.1',
      packages=find_packages(),
      author=u'Adam Cupiał',
      url='https://github.com/adamcupial/django-html5-forms',
      include_package_data=True,
      description=DESCRIPTION,
      long_description=LONG_DESCRIPTION,
      platforms=['any'],
      classifiers=[
          'Development Status :: 4 - Beta',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: MIT License',
          'Operating System :: OS Independent',
          'Programming Language :: Python',
          'Topic :: Text Processing :: Markup :: HTML',
          'Topic :: Software Development :: Libraries :: Python Modules',
      ],
)
