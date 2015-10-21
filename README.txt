 _        _     _                  _ 
| |_ __ _| |__ | |_ ___  ___  __ _| |
| __/ _` | '_ \| __/ _ \/ __|/ _` | |
| || (_| | |_) | || (_) \__ \ (_| | |
 \__\__,_|_.__/ \__\___/|___/\__, |_|
                                |_|  

Simple Tableau SQL Extract Tool


OVERVIEW:
tabtosql is a simple command line tool for parsing sql queries & related
information out of tableau workbooks (.twb & .twbx files). It works by
taking a tableau workbook, parsing the xml, and writing the information
about worksheets, connections to those worksheets, their connection(db)
details, and the corresponding custom sql (assuming it exists) to disk.

To run, simply pip install (See: INSTALL), then run (See: USAGE) in the 
console of your choice. The CLI takes two arguments, the input file
(.twb(x)) and the output file (.sql). Current implementation has only 
been tested on Python 3.4+. Minimal exceptions have been handled for.


REQUIREMENTS:
- Python 3.4+
- requirements.txt


INSTALL:
$ python -m pip install git+https://github.com/LeviKanwischer/tabtosql


USAGE:
$ tabtosql -i input.twb(x) -o output.sql


STRUCTURE:
tabtosql
├── README.txt
├── LICENSE.txt
├── requirements.txt
├── setup.py
└── tabtosql
    ├── __init__.py
    ├── __main__.py
    └── tabtosql.py


TODO:
- Test/Add Python 2.7+ compatibility
- Add ability to pull workbook from server (REST API)
 