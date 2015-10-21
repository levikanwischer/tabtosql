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

import click
from tabtosql import tabtosql


@click.command()
@click.option('--infile', '-i', prompt=True, help='Input file (.twb(x))')
@click.option('--outfile', '-o', prompt=True, help='Output file (.sql)')
def cli(infile, outfile):
    """
    Simple Tableau SQL Extract Tool\n
    -------------------------------\n
    tabtosql is a simple command line tool for parsing sql queries & related
    information out of tableau workbooks (.twb & .twbx files). It works by
    taking a tableau workbook, parsing the xml, and writing the information
    about worksheets, connections to those worksheets, their connection(db)
    details, and the corresponding custom sql (assuming it exists) to disk.
    """
    twb = tabtosql.return_xml(infile)

    worksheets = tabtosql.parse_worksheets(twb.find('worksheets'))
    datasources = tabtosql.parse_datasources(twb.find('datasources'))
    sql = tabtosql.parse_queries(twb.find('datasources'))

    output = tabtosql.format_header(infile)
    output += tabtosql.format_worksheets(worksheets)
    output += tabtosql.format_datasources(datasources)
    output += tabtosql.format_queries(sql)

    with open(outfile, 'wb') as f_out:
        f_out.write(output.encode('utf-8'))
