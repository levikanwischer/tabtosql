# -*- coding: utf-8 -*-

"""
Tableau Workbook SQL Extract Tool

tabtosql is a command line tool for parsing sql queries & related
information out of tableau workbooks (.twb & .twbx files). It works by
taking a tableau workbook, parsing the xml, and formatting information
about worksheets, connections to those worksheets, their connection(db)
details, and the corresponding custom sql (assuming it exists) in a
valid sql & human readable format.

    USAGE:
    $ tabtosql input.twb(x) > output.sql

See the README for further details.
"""

from .workbook import convert


__title__ = 'tabtosql'
__version__ = '1.0.3'
__author__ = 'Levi Kanwischer'
__copyright__ = 'Copyright (c) 2016 Levi Kanwischer'
__license__ = 'MIT'
__all__ = ['convert']
