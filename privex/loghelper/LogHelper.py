"""
Copyright 2018     Privex Inc.

Permission is hereby granted, free of charge, to any person obtaining a copy of 
this software and associated documentation files (the "Software"), to deal in 
the Software without restriction, including without limitation the rights to use, 
copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the 
Software, and to permit persons to whom the Software is furnished to do so, 
subject to the following conditions:

The above copyright notice and this permission notice shall be included in all 
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, 
INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A 
PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT 
HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION 
OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE 
SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

import sys
import datetime
import logging
from logging.handlers import TimedRotatingFileHandler

class LogHelper:
    """
    LogHelper is a small class written by Chris (Someguy123) @ Privex Inc. to simplify the use of 
    the built-in Python Logging Module.

    It has no dependencies, and should be compatible with most versions of 
    Python 2.x and 3.x (though we still recommend a minimum of 3.4).

    :author:    Someguy123 (Chris) @ Privex Inc.
                https://github.com/Someguy123 - https://github.com/Privex
    :license:   MIT
    :source:    https://github.com/Privex/python-loghelper
    """
    def __init__(self, logger_name = '', level = logging.DEBUG, handler_level = logging.INFO, formatter = None):
        # type: (str, int, int, logging.Formatter) -> None
        """
        Initialises the class with sensible default values, including a default formatter, a global log level
        of DEBUG, with a handler default level of INFO.

        There's no need to even pass any variables to the constructor unless you're customising something.
        However, you may want to change the logger name to avoid potential conflicts with the default root logger.

        Basic usage:

            Create an instance of LogHelper. Customise any kwargs as needed.
            >>> lh = LogHelper(logger_name='myapp.someclass', handler_level=logging.DEBUG)
            Add one or more handlers (you can mix and match, e.g. console and file).
            >>> lh.add_file_handler('myapp.log')
            Once you're done adjusting your logger, just grab the logging instance and use it.
            >>> log = lh.get_logger()
            >>> log.info('hello world')

            Now `myapp.log` will contain:

                2018-12-05 14:50:41,902 myapp.someclass    INFO    hello world

        :param logger_name:     Name of the logger to use (used by getLogger).
        :param level:           Global logging level. This must be more verbose than your handlers, or they
                                will be silenced.
        :param handler_level:   Default logging level for added handlers. Can be overridden from the methods.
        :param formatter:       An instance of :py:class:`logging.Formatter`
        """
        self.handler_level = handler_level
        self.level = level
        self.logger_name = logger_name

        # Sensible default formatter if you don't pass one
        # Messages are formatted like this:
        #
        #   2018-12-05 14:50:41,902 my.logger.name    ERROR    my error message
        #
        self.formatter = logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s %(message)s')

        if formatter is not None:
            self.formatter = formatter

        self.log = logging.getLogger(logger_name)
        self.log.setLevel(self.level)

    def get_logger(self):
        # type: () -> logging.Logger
        """
        Return the Logger instance once you're done adding handlers and other customisations.

        :return: Instance of :py:class:`logging.Logger`
        """
        return self.log

    def add_file_handler(self, file_location, level=None, formatter=None):
        # type: (str, int, logging.Formatter) -> logging.FileHandler
        """
        Outputs logs matching the given `level` using `formatter` into the file `file_location`.

        If you need rotation, check :py:func:`LogHelper.add_timed_file_handler`

        Creates a FileHandler using the given parameters, uses sensible defaults for level/formatter if no
        parameters were passed, then adds the handler to `self.log`.

        :param file_location:   Relative or (ideally) absolute location to log file to save to.
        :param level:           Logging level for the handler, e.g. logging.INFO. Defaults to self.handler_level
        :param formatter:       For adjusting the logging format of this handler. Defaults to self.formatter.
                                An instance of :py:class:`logging.Formatter`
        :return:                The newly generated instance of :py:class:`logging.FileHandler`
        """
        handler = logging.FileHandler(file_location)
        handler.setLevel(self.handler_level if level is None else level)
        handler.setFormatter(self.formatter if formatter is None else formatter)

        self.log.addHandler(handler)
        return handler

    def add_timed_file_handler(self, file_location, when='D', interval=1, backups=14, at_time=None,
                               level=None, formatter=None):
        # type: (str, str, int, int, datetime.time, int, logging.Formatter) -> TimedRotatingFileHandler
        """
        Outputs logs matching the given `level` using `formatter` into the file `file_location`. Rotates log every
        x intervals, (`when` sets type, `interval` sets count). Removes logs older than `backups` intervals.

        By default, logs are rotated once (interval=1) per day (when='D'), and removed after 14 days (backups=14).

        Creates a TimedRotatingFileHandler using the given parameters, uses sensible defaults for level/formatter if no
        parameters were passed, then adds the handler to `self.log`.

        :param file_location:   Relative or (ideally) absolute location to log file to save to.

        :param when:            String value defining the type of interval, e.g. D for days, S for seconds
                        More info: https://docs.python.org/3.7/library/logging.handlers.html#timedrotatingfilehandler

        :param interval:        How many `when`'s before rotating the log? (default 1 day)
        :param backups:         How many intervals should be kept before deletion? (default 14 days)
        :param at_time:         Only used for `midnight` and `W0-W6` interval types. Instance of :py:func:`datetime.time`

        :param level:           Logging level for the handler, e.g. logging.INFO. Defaults to self.handler_level
        :param formatter:       For adjusting the logging format of this handler. Defaults to self.formatter.
                                An instance of :py:class:`logging.Formatter`
        :return:                The newly generated instance of :py:class:`logging.handlers.TimedRotatingFileHandler`
        """
        handler = TimedRotatingFileHandler(
            file_location, when=when, interval=interval, backupCount=backups, atTime=at_time
        )

        handler.setLevel(self.handler_level if level is None else level)
        handler.setFormatter(self.formatter if formatter is None else formatter)

        self.log.addHandler(handler)
        return handler

    def add_console_handler(self, level=None, formatter=None):
        # type: (int, logging.Formatter) -> logging.StreamHandler
        """
        Outputs logs matching the given `level` using `formatter` into standard output (console).

        :param level:           Logging level for the handler, e.g. logging.INFO. Defaults to self.handler_level
        :param formatter:       For adjusting the logging format of this handler. Defaults to self.formatter.
                                An instance of :py:class:`logging.Formatter`
        :return:                The newly generated instance of :py:class:`logging.FileHandler`
        """
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(self.handler_level if level is None else level)
        handler.setFormatter(self.formatter if formatter is None else formatter)
        self.log.addHandler(handler)
        return handler




