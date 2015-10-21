# -*- coding: utf-8 -*-

"""
tabtosql.tabtosql
-----------------
This module contains logic for parsing tableau workbooks to valid sql.

    USAGE:
    >>> tabtosql.tabtosql.*

See the README.txt for further details.
"""

import os
import getpass
import zipfile
from datetime import datetime
import xml.etree.ElementTree as ET
from collections import OrderedDict


BIG_LINE = 77
SMALL_LINE = 50


def return_xml(infile):
    """Load twb XML into memory & return root object."""
    if infile.endswith('.twbx'):
        infile = _parse_twbx(infile)
    return ET.parse(infile).getroot()


def _parse_twbx(infile):
    """Parse twbx zip & return twb XML object."""
    with open(infile, 'rb') as f_in:
        twbx = zipfile.ZipFile(f_in)
        for item in twbx.namelist():
            if item.endswith('.twb'):
                return twbx.open(item)


def parse_worksheets(worksheets):
    """Parse worksheet xml objects & return cleaned values."""
    results = OrderedDict()
    for worksheet in worksheets:
        name = worksheet.attrib['name']
        datasource = worksheet.find('table/view/datasources')
        datasource = [i.attrib['caption'] for i in datasource if 'caption' in i.attrib]
        results[name] = datasource
    return results


def parse_datasources(datasources):
    """Parse connection xml objects & return cleaned values."""
    results = OrderedDict()
    datasources = [i for i in datasources if 'caption' in i.attrib]
    for datasource in datasources:
        name = datasource.attrib['caption']
        datasource = datasource.find('connection')
        engine = datasource.attrib['class'] if 'class' in datasource.attrib else None
        database = datasource.attrib['dbname'] if 'dbname' in datasource.attrib else None
        server = datasource.attrib['server'] if 'server' in datasource.attrib else None
        username = datasource.attrib['username'] if 'username' in datasource.attrib else None
        results[name] = {'engine': engine, 'db': database, 'server': server, 'user': username}
    return results


def parse_queries(datasources):
    """Parse query&table xml objects & return cleaned values."""
    results = OrderedDict()
    datasources = [i for i in datasources if 'caption' in i.attrib]
    for datasource in datasources:
        name = datasource.attrib['caption']
        query = datasource.find('connection/relation')
        query = query.text if query.text else '-- LINKED TO: {}'.format(query.attrib['table'])
        # Cleans eval operators that are manipulated by tableau for XML
        query = query.replace('<<', '<').replace('>>', '>')
        results[name] = query
    return results


def format_header(infile):
    """Format header object for outfile."""
    infile = os.path.abspath(infile)
    username = getpass.getuser()
    today = datetime.now().strftime('%Y-%m-%d %I:%M%p')
    output = '{}\n'.format('-'*BIG_LINE)
    output += '-- Created by: {}\n'.format(username)
    output += '-- Created on: {}\n'.format(today)
    output += '-- Source: {}\n'.format(infile)
    output += '{}{}'.format('-'*BIG_LINE, '\n'*3)
    return output


def format_worksheets(worksheets):
    """Format worksheets object for outfile."""
    output = '-- Worksheets w/ Datasources {}\n'.format('-'*(BIG_LINE-29))
    for worksheet in worksheets:
        output += '-- {}\n'.format(worksheet)
        for source in worksheets[worksheet]:
            output += '  -- {}\n'.format(source)
        output += '\n'
    output += '\n'*2
    return output


def format_datasources(datasources):
    """Format datasources object for outfile."""
    output = '-- Datasources & Connections {}\n'.format('-'*(BIG_LINE-29))
    for source in datasources:
        output += '-- {}\n'.format(source)
        output += '  -- Server: {}\n'.format(datasources[source]['server'])
        output += '  -- Engine: {}\n'.format(datasources[source]['engine'])
        output += '  -- Database: {}\n'.format(datasources[source]['db'])
        output += '  -- Username: {}\n'.format(datasources[source]['user'])
        output += '\n'*2
    return output


def format_queries(queries):
    """Format datasources object for outfile."""
    output = '-- Queries {}\n'.format('-'*(BIG_LINE-11))
    for query in queries:
        output += '-- {} {}\n'.format(query, '-'*(SMALL_LINE-4-len(query)))
        output += queries[query]
        output += '\n;{}'.format('\n'*3)
    return output
