# -*- coding: utf-8 -*-

from distutils.core import setup

import os
import tabtosql


def _load(filename):
    """Load file contents from package base path."""
    base = os.path.dirname(os.path.abspath(__file__))
    loadfile = os.path.join(base, filename)
    with open(loadfile, 'r') as f_in:
        return f_in.read()


readme = _load('README.txt')
requires = [i for i in _load('requirements.txt').split('\n') if i.strip()]


classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Environment :: Console',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3 :: Only',
    'Topic :: Utilities'
    ]


setup(name=tabtosql.__title__,
      version=tabtosql.__version__,
      license=tabtosql.__license__,
      description='Simple Tableau SQL Extract Tool',
      long_description=readme,
      author=tabtosql.__author__,
      url='https://github.com/LeviKanwischer/tabtosql',
      packages=['tabtosql'],
      install_requires=requires,
      entry_points={'console_scripts': ['tabtosql = tabtosql.__main__:cli']},
      classifiers=classifiers
      )
