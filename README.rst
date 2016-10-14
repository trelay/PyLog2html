PyLog2html
==========

Support both Python2 and Python3

PyLog2Html can save log to HTML file, there is plenty of reasons to save log into HTML file:

* Highlight errors
* Colorful output
* More readable
* Insert table

Installation
------------

Install with pip::

    pip install PyLog2html

Quick Start
-----------

.. code-block:: python

    from HTMLLogger import HTMLLogger
    logger=HTMLLogger(name="Test App", html_filename="log.html", console_log=True)
    logger.info('This is info')
    logger.debug('This is debug')
    logger.warning("This is <hl>warning</hl>")
    logger.error('This is an <hl>error</hl>')
    logger.table('Add html table:<table><tr><th>...</th></tr></table>')

View the log:
-------------

* Open log file "log.html" in browser, it takes a while to open the log file, it depends on the performance of your computer.
* Select a level name to dedicate on particular messages.
* Or type a keyword to find your interesting message(select checkbox to mismatch case)
* If you set console_log to True when you'll see the log would also print to console

Version
-------

1.0.3

Class Inheritance:
------------------

* [HTMLFileHandler]: The derived class of Python logging.handlers.RotatingFileHandler
* [HTMLFormatter]: The derived class of Python logging.Formatter
* [CONFormatter]: The derived class of Python logging.Formatter


HTMLFileHandler
---------------

The sub class of logging.handlers.RotatingFileHandler, you can see this class is to extend the function of Rotating HTML file, comparing to its parent class, it has following advantages:

* The format of log file name will be saved as "log_1.html" & "log_2.html". 
* Write the beginning and end strings in HTML, like "\<html>\<head>...\</head>\</html>"
* Have a switch to let user choose if need to rotate files: If it's False, the log file will be added and rollover occurs whenever the current log file is nearly maxBytes in length. If it's True, it behaves like logging.handlers.RotatingFileHandler.


HTMLFormatter
-------------

The sub class of logging.Formatter, you can see this class is to add HTML tags, comparing to its parent class, it has following advantages:

* Highlight keyword by setting its size and the Italic
* Find the correct color to display for particular messages in Html file.
* The keyword should be decorated by <hl>keyword</hl>(which can be found in config file or variables you defined.)

CONFormatter
------------

The sub class of logging.Formatter, this module is to print log to console with color if console_log was set to True when you instance class PyLogger and raise errors if the color you chose is not supported by Console.

Currently, Only following color are supported in Console:

 * yellow
 * cyan
 * magenta
 * blue
 * orange
 * green
 * red
 * black
 * white
 * normal

HTMLLogger
----------
The main logger creator, the sub class of logging.Logger, use to instance a single logging channel. By default, you should use this class rather than use logging.Logger. If you'd like to create a logger with the specified name, you should call function <logging.getLogger> and add HTMLFormatter and HTMLFileHandler using addFilter and addHandler.

The config
----------

You have two options here: 

* Use `oslo.config <http://docs.openstack.org/developer/oslo.config/>`_ , and read variables from the config file
* Set Variables in your script.

An example:

.. code-block:: python

    from HTMLLogger import HTMLLogger

    app_name="Red_Fish"
    Keyword_Italic=True
    Keyword_FontSize=5
    HighLight_msg_tag_start="<hl>"
    HighLight_msg_tag_end="</hl>"
    msg_color=dict(
    err_color="magenta",
    warn_color="orange",
    info_color="white",
    dbg_color="white")
    log_format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s'
    HtmlmaxBytes=1024*1024*5
    console_log=True
    html_title="Default Title"
    html_filename="Redfish_log.html"

    logger=PyLogger(name=app_name, html_filename=html_filename, mode='a',
    html_title=html_title,level=logging.DEBUG,
    HtmlmaxBytes=HtmlmaxBytes, encoding=None, delay=False,
    html_format=log_format, msg_color=msg_color,
    Keyword_Italic=Keyword_Italic,Keyword_FontSize=Keyword_FontSize,
    HighLight_msg_tag_start=HighLight_msg_tag_start,
    HighLight_msg_tag_end=HighLight_msg_tag_end,console_log=console_log,
    Html_Rotating=False,Html_backupCount=5)

    logger.debug('This is debug')
    logger.info('This is info')
    logger.warning("This is <hl>warning</hl>")
    logger.error('This is <hl>error</hl> xxx')
    logger.table('Add html table:<table><tr><th>...</th></tr></table>')


**Free Software, Hell Yeah!**

.. (Contact trelwan@celestica.com if you have any questions.)

