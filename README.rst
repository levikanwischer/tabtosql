:: 

     _        _     _                  _ 
    | |_ __ _| |__ | |_ ___  ___  __ _| |
    | __/ _` | '_ \| __/ _ \/ __|/ _` | |
    | || (_| | |_) | || (_) \__ \ (_| | |
     \__\__,_|_.__/ \__\___/|___/\__, |_|
                                    |_|  



*Tableau Workbook SQL Extract Tool*


.. image:: https://img.shields.io/pypi/v/tabtosql.svg
    :target: https://pypi.python.org/pypi/tabtosql


OVERVIEW
''''''''
tabtosql is a command line tool for parsing sql queries & related
information out of tableau workbooks (.twb & .twbx files). It works by
taking a tableau workbook, parsing the xml, and formatting information
about worksheets, connections to those worksheets, their connection(db)
details, and the corresponding custom sql (assuming it exists) in a
valid sql & human readable format.


USAGE
'''''
.. code-block:: bash

    $ tabtosql input.twb(x) > output.sql


INSTALL
'''''''
.. code-block:: bash

    $ python -m pip install tabtosql
