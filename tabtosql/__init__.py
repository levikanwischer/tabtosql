# -*- coding: utf-8 -*-

"""
Simple Tableau SQL Extract Tool
-------------------------------
tabtosql is a simple command line tool for parsing sql queries & related
information out of tableau workbooks (.twb & .twbx files). It works by
taking a tableau workbook, parsing the xml, and writing the information
about worksheets, connections to those worksheets, their connection(db)
details, and the corresponding custom sql (assuming it exists) to disk.

    USAGE:
    $ tabtosql -i input.twb(x) -o output.sql

See the README.txt for further details.
"""

__title__ = 'tabtosql'
__version__ = '1.0.0'
__author__ = 'Levi Kanwischer'
