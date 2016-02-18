# -*- coding: utf-8 -*-

"""Tableau Workbook SQL Extract Tool"""

import codecs
import os
import re
from setuptools import setup, find_packages


NAME = 'tabtosql'


def read(filename):
    """Load file contents from setup.py path."""
    here = os.path.dirname(os.path.abspath(__file__))
    filepath = os.path.join(here, filename)
    if not os.path.isfile(filepath):
        raise OSError('%s missing from `%s` source.' % (filename, NAME))

    with codecs.open(filepath, encoding='utf-8') as infile:
        return infile.read()


def version(baked='0.0.0.dev1'):
    """Extract package version metadata."""
    regex = r'''__version__\s*=\s*['\"]([^'\"]*)['\"]'''
    source = read(os.path.join(NAME, '__init__.py'))
    match = re.search(regex, source, re.M)
    return match.group(1) if match else baked


CLASSIFIERS = ['Development Status :: 5 - Production/Stable',
               'Environment :: Console',
               'Intended Audience :: Developers',
               'License :: OSI Approved :: MIT License',
               'Natural Language :: English',
               'Operating System :: OS Independent',
               'Programming Language :: Python',
               'Programming Language :: Python :: 2',
               'Programming Language :: Python :: 2.6',
               'Programming Language :: Python :: 2.7',
               'Programming Language :: Python :: 3',
               'Programming Language :: Python :: 3.4',
               'Programming Language :: Python :: 3.5',
               'Topic :: Utilities',
              ]


setup(name=NAME,
      version=version(baked='1.0.0rc1'),
      author='Levi Kanwischer',
      author_email='levi@kanwischer.me',
      license='MIT',
      url='https://github.com/LeviKanwischer/%s' % NAME,
      description=__doc__,
      long_description=read('README.rst'),
      classifiers=CLASSIFIERS,
      install_requires=['click>=4.1'],
      entry_points={'console_scripts': ['tabtosql = tabtosql.__main__:cli']},
      packages=find_packages(),
     )
