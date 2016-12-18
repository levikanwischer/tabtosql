# -*- coding: utf-8 -*-

"""tabtosql.workbook

This module contains logic for parsing tableau workbooks to valid sql.


See the README for further details.

"""

import getpass
import os
import re
import xml.etree.ElementTree as ET
import zipfile
from collections import OrderedDict
from datetime import datetime


LINE_BIG = 77
LINE_SMALL = 50


def return_xml(filename):
    """Load twb XML into memory & return root object.

    Parameters
    ----------
    filename : str
        Path to Tableau file to convert.

    Returns
    -------
    xml : object <ElementTree>
        Root ET object from initial Tableau file.

    """
    _validate_file(filename)

    if filename.endswith('.twbx'):
        xml = _parse_twbx(filename)
        return xml

    xml = ET.parse(filename).getroot()
    return xml


def _validate_file(filename):
    """Validate given file is acceptable for processing.

    Parameters
    ----------
    filename : str
        Path to Tableau file to convert.

    Raises
    ------
    OSError
        If given `filename` is not a valid file.
        If given `filename` is not a .twb(x) file.

    """
    if not os.path.isfile(filename):
        raise OSError('%s is not a valid file path.' % filename)

    if filename.split('.')[-1] not in ('twb', 'twbx'):
        raise OSError('%s is not a valid tableau file.' % filename)


def _parse_twbx(filename):
    """Parse twbx zip & return twb XML.

    Parameters
    ----------
    filename : str
        Path to Tableau file to convert.

    Returns
    -------
    xml : object <ElementTree>
        Root ET object from initial Tableau file.

    """
    with open(filename, 'rb') as infile:
        twbx = zipfile.ZipFile(infile)

        for item in twbx.namelist():
            if item.endswith('.twb'):
                twb = twbx.open(item)
                xml = ET.parse(twb).getroot()
                return xml


def parse_worksheets(worksheets):
    """Parse worksheet xml objects & return cleaned values.

    Parameters
    ----------
    worksheets : array-like <list>
        List of worksheet XML objects to parse.

    Returns
    -------
    results : array-like <OrderedDict>
        Dictionary of datasources from worksheets.

    """
    results = OrderedDict()

    for worksheet in worksheets:
        name = worksheet.attrib['name']
        datasource = worksheet.find('table/view/datasources')
        datasource = [i.attrib['caption'] for i in datasource if 'caption' in i.attrib]
        results[name] = datasource

    return results


def parse_datasources(datasources):
    """Parse connection xml objects & return cleaned values.

    Parameters
    ----------
    datasource : array-like <dict>
        Dictionary of datasources from worksheets.

    Returns
    -------
    results : array-like <OrderedDict>
        Dictionary of connection details for datasources.

    """
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
    """Parse query&table xml objects & return cleaned values.

    Parameters
    ----------
    datasource : array-like <dict>
        Dictionary of datasources from worksheets.

    Returns
    -------
    results : array-like <OrderedDict>
        Dictionary of queries from datasources.

    """
    results = OrderedDict()
    datasources = [i for i in datasources if 'caption' in i.attrib]

    for datasource in datasources:

        name = datasource.attrib['caption']
        conn = datasource.find('connection/relation')
        query = conn.text if conn.text else '-- LINKED TO: %s' % conn.attrib['table']

        query = query.replace('<<', '<').replace('>>', '>')

        # TODO: Should be handling for universal newlines better (ie \r\n)
        results[name] = re.sub(r'\r\n', r'\n', query)

    return results


def format_header(filename):
    """Format header object for outfile.

    Parameters
    ----------
    worksheets : array-like <list>
        List of worksheet XML objects to parse.

    Returns
    -------
    output : str
        Formatted header metadata for outfile.

    """
    filename = os.path.abspath(filename)
    username = getpass.getuser()
    today = datetime.now().strftime('%Y-%m-%d %I:%M%p')

    output = '%s\n' % ('-'*LINE_BIG)
    output += '-- Created by: %s\n' % username
    output += '-- Created on: %s\n' % today
    output += '-- Source: %s\n' % filename
    output += '%s%s' % ('-'*LINE_BIG, '\n'*3)

    return output


def format_worksheets(worksheets):
    """Format worksheets object for outfile.

    Parameters
    ----------
    worksheets : array-like <list>
        List of worksheet XML objects to parse.

    Returns
    -------
    output : str
        Formatted worksheet details for outfile.

    """
    output = '-- Worksheets w/ Datasources %s\n' % ('-'*(LINE_BIG-29))

    for worksheet in worksheets:
        output += '-- %s\n' % worksheet

        for source in worksheets[worksheet]:
            output += '  -- %s\n' % source

        output += '\n'

    output += '\n'*2
    return output


def format_datasources(datasources):
    """Format datasources object for outfile.

    Parameters
    ----------
    datasource : array-like <dict>
        Dictionary of datasources from worksheets.

    Returns
    -------
    output : str
        Formatted datasource details for outfile.

    """
    output = '-- Datasources & Connections %s\n' % ('-'*(LINE_BIG-29))

    for source in datasources:
        output += '-- %s\n' % source
        output += '  -- Server: %s\n' % datasources[source]['server']
        output += '  -- Engine: %s\n' % datasources[source]['engine']
        output += '  -- Database: %s\n' % datasources[source]['db']
        output += '  -- Username: %s\n' % datasources[source]['user']
        output += '\n'*2

    return output


def format_queries(queries):
    """Format datasources object for outfile.

    Parameters
    ----------
    queries : array-like <dict>
        Dictionary of queries from worksheets.

    Returns
    -------
    output : str
        Formatted query details for outfile.

    """
    output = '-- Queries %s\n' % ('-'*(LINE_BIG-11))

    for query in queries:
        output += '-- %s %s\n' % (query, '-'*(LINE_SMALL-4-len(query)))
        output += queries[query]
        output += '\n;%s' % ('\n'*3)

    return output


def convert(filename):
    """Process tableau to sql conversion.

    Parameters
    ----------
    filename : str
        Path to Tableau file to convert.

    Returns
    -------
    output : str
        Fully formatted output from initial Tableau file.

    """
    twb = return_xml(filename)

    worksheets = parse_worksheets(twb.find('worksheets'))
    datasources = parse_datasources(twb.find('datasources'))
    sql = parse_queries(twb.find('datasources'))

    output = format_header(filename)
    output += format_worksheets(worksheets)
    output += format_datasources(datasources)
    output += format_queries(sql)

    return output
