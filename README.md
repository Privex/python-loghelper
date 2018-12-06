# Python Log Helper

**Python Log Helper** is a small class designed to simplify the use of the built-in Python Logging Module.

It has no dependencies, and should be compatible with most versions of Python 2.x and 3.x (though we still recommend a minimum of 3.4).

It was originally created by [Chris (Someguy123)](https://github.com/Someguy123) for use in personal Python projects, 
as well as for use in projects developed at [Privex Inc.](https://github.com/Privex)

**If this project has helped you, consider [grabbing a VPS or Dedicated Server from Privex](https://www.privex.io) - prices start at as little as 8 USD/mo (we take cryptocurrency!)**

# License

**Python Log Helper** was created by [Privex Inc. of Belize City](https://www.privex.io), and licensed under the MIT License. See the file [LICENSE](LICENSE) for the license text.

**TL;DR; license:**

We offer no warranty. You can copy it, modify it, use it in projects with a different license, and even in commercial (paid for) software.

The most important rule is - you **MUST** keep the original license text visible (see `LICENSE`) in any copies.

# Contributing

We're happy to accept pull requests, no matter how small.

Please make sure any changes you make meet these basic requirements:

 - No additional dependencies. We want LogHelper to be lightweight and painless to install.
 - Any code taken from other projects should be compatible with the MIT License
 - This is a new project, and as such, supporting Python versions prior to 3.4 is very low priority.
 - However, we're happy to accept PRs to improve compatibility with older versions of Python, as long as it doesn't:
   - drastically increase the complexity of the code
   - OR cause problems for those on newer versions of Python.

# Installation

### Manual install from Git

**Option 1 - Use pip to install straight from Github**

```sh
pip3 install git+https://github.com/Privex/python-loghelper
```

**Option 2 - Clone and install manually**

```bash
# Clone the repository from Github
git clone https://github.com/Privex/python-loghelper
cd python-loghelper

# RECOMMENDED INSTALL METHOD
# Use pip to install the source code
pip3 install .

# ALTERNATIVE INSTALL METHOD
# If you don't have pip, or have issues with installing using it, then you can use setuptools instead.
python3 setup.py install
```

# Usage

The code is very well documented, you can find out all usage documentation in [LogHelper.py](privex/loghelper/LogHelper.py).

All functions are type annotated, with detailed pydoc block comments. If you're using a Python optimised IDE such as [PyCharm](https://www.jetbrains.com/pycharm/) it should
offer code completion and help when using the package.

### Basic usage

The most basic usage is to simply initialise the class with no parameters, and attach a 
file handler to send log output to a file.

```python
# Import the class
from privex.loghelper import LogHelper
lh = LogHelper()
# Log to a file called test.log in the current directory
lh.add_file_handler('test.log')
# Grab the logger instance
log = lh.get_logger()
# Now let's log 'hello world' to the file.
log.info('hello world')
```

After running the above, `test.log` should contain:

```
2018-12-05 22:05:18,915 root         INFO     hello world
```

### Splitting error and debug logs into different files

Something that can make it easier to sift through logs, is to split your normal debug logs from warnings and errors.

Using the standard `logging` module, this could take 10 lines of code, and is highly repetitive.

With the Python Log Helper, it's just a few lines.

```python
# Import the class
from privex.loghelper import LogHelper
# Import logging to be able to specify the verbosity levels
import logging

# The global level (kwarg `level`) defaults to DEBUG, but the default handler level is only INFO.
# You can specify handler_level to change that. 
# To help prevent conflicts from other python packages which use the root ('') logger, you should set a custom
# logger name.
lh = LogHelper(logger_name='my_app', handler_level=logging.DEBUG)

# Log messages that are DEBUG (default handler and global logging level) or higher to `debug.log`
lh.add_file_handler('debug.log')

# Log only WARNING or above to `error.log`
lh.add_file_handler('error.log', level=logging.WARNING)

# Grab the logger instance
log = lh.get_logger()

# To test that logs are being sent to the correct files, let's try an `info`, a `warning` and an `error` log message.
log.info('something normal is happening')
log.warning('something strange is happening')
log.error('something VERY BAD is happening')

```

After running the above Python script, you should see the following log files:

**debug.log**

```
2018-12-05 22:10:25,253 root         INFO        something normal is happening
2018-12-05 22:10:25,254 root         WARNING     something strange is happening
2018-12-05 22:10:25,256 root         ERROR       something VERY BAD is happening
```

**error.log**

```
2018-12-05 22:10:25,254 root         WARNING     something strange is happening
2018-12-05 22:10:25,256 root         ERROR       something VERY BAD is happening
```

As you can see, the `debug.log` saved all of the messages, while `error.log` only saved the warning and the error.

### Log Rotation

You can also have painless log rotation, without the need for something like `logrotated`.

The LogHelper class has a function `add_timed_file_handler` which wraps `logging.handler.TimedRotatingFileHandler`.



Simply specify the type of interval (`when`) to rotate with, how often it should rotate (`interval`), and how many intervals you
would like to keep before deleting older ones (`backups`). Set `backups` to 0 if you don't want it to delete older logs.

For more information on `interval`, `when` and `backups`, 
see [the official logging docs](https://docs.python.org/3.7/library/logging.handlers.html#timedrotatingfilehandler)

By default, logs are rotated once (interval=1) per day (when='D'), and removed after 14 days (backups=14).

```python
# Import the class
from privex.loghelper import LogHelper
# Using sleep to simulate time passing
from time import sleep
lh = LogHelper()
# Log to a file called test.log in the current directory
# Rotate the log every minute, and only keep up to 60 minutes of logs
lh.add_timed_file_handler('test.log', when='M', interval=1, backups=60)
# Grab the logger instance
log = lh.get_logger()
# Now let's log 'hello world' to the file.
log.info('hello world')
log.info('hello world 2')
sleep(60)
log.info('hello world 3')
```

We can now see it's generated two timestamped logs, since the interval was set to 1 minute.

```bash
$ ls -l
    -rw-r--r--  1 user  users    58  5 Dec 22:58 test.log.2018-12-05_22-58
    -rw-r--r--  1 user  users    58  5 Dec 22:59 test.log.2018-12-05_22-59

$ cat test.log.2018-12-05_22-58
    2018-12-05 22:58:24,600 root         INFO     hello world
    2018-12-05 22:58:24,743 root         INFO     hello world 2

$ cat test.log.2018-12-05_22-59
    2018-12-05 22:59:25,512 root         INFO     hello world 3
```

# Thanks for reading!

**If this project has helped you, consider [grabbing a VPS or Dedicated Server from Privex](https://www.privex.io) - prices start at as little as US$8/mo (we take cryptocurrency!)**