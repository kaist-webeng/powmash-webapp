# PowMash User Interface Web Application

## Prerequisites

* Python 3.5+
* [pip](https://pip.pypa.io/en/stable/)
* [Mono framework](http://www.mono-project.com/)
* [Node-RED](http://nodered.org/)

## Setting the Environment

It is *highly recommended* to create a Python virtual environment to run this
web application using [venv](https://docs.python.org/3/library/venv.html) or 
[virtualenv](https://pypi.python.org/pypi/virtualenv). If you are already using
other version of Python than 3.5+, it is recommended to use Python version
manager such as [pyenv](https://github.com/yyuu/pyenv) or
[p](https://github.com/qw3rtman/p).

If you are set with the prerequisites, install the dependencies.

```
$ pip install -r requirements.txt
```

You should configure the application settings before running the application.
This application reads the configuration from a file whose path is the value
of environment variable `POWMASH_WEBAPP_SETTINGS`.

There is an example for application settings file, named
`settings.example.py`. Copy this file, edit the copied file, and set the value
of environment variable `POWMASH_WEBAPP_SETTINGS` to the path to the copied
file. In POSIX environment, you can do like this before executing the script:

```
$ export POWMASH_WEBAPP_SETTINGS=/path/to/settings.you.py
```

## Running the Application

It's just a simple [Flask](http://flask.pocoo.org/) application. The simplest
way is:

```
$ python powmash-webapp.py
```

## Developing

A PyCharm project directory exists in this repository. If you are free with
PyCharm, it's just okay to open the root directory in PyCharm to do your work.
