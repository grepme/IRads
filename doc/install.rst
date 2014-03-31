Installation
============


System Requirements
-------------------

* `Python 2 (2.6+) <https://www.python.org/>`_
    * If you don't currently have Python installed on your system, the `Python documentation <http://docs.python.org/2/>`_ contains installation instructions for all major operating systems.

* `MySQL <http://www.mysql.com/>`_
    * See the `MySQL documentation <http://dev.mysql.com/doc/refman/5.6/en/installing.html>`_ for installation instructions.

* `CherryPy <http://www.cherrypy.org/>`_
    * Easiest installed with `pip <https://pypi.python.org/pypi/pip>`_ (if needed, follow that link for installation instructions). Using pip, simply run ``pip install CherryPy``

* `Mako Templates <http://www.makotemplates.org/>`_
    * Installation via pip: ``pip install Mako``

* `Pillow <http://python-imaging.github.io/>`_
    * Read the `documentation <http://pillow.readthedocs.org/en/latest/installation.html>`_ on how to install as Pillow requires various pre-requisites (for this application, at minimum `libjpeg <http://libjpeg.sourceforge.net/>`_, is required)

* `SQLAlchemy <http://www.sqlalchemy.org/>`_
    * Installation via pip: ``pip install SQLAlchemy``


Installation & Configuration
----------------------------

To install Irads, simply extract the archive into a folder of your choice.

Configuration is done through the ``config.py`` file: simply open it in a text editor and add in the necessary information (MySQL database information and IP/port settings). Irads does not create the database for you so make sure it is already set up before launching.


Launching Irads
---------------

To launch Irads on Windows, navigate in a command prompt to the directory where it has been extracted, and run ``python iradsmain.py``. If this command fails, you will most likely have to `set your environment variables first <http://docs.python.org/2/using/windows.html#excursus-setting-environment-variables>`_.
To launch Irads on Mac OSX or Linux, navigate in a terminal to the directory where it has been extracted, then run ``chmod +x iradsmain.py`` (the first time) and ``./iradsmain.py`` to launch. If this fails, `make sure /usr/bin/python points to the right executable <http://docs.python.org/2/using/unix.html#python-related-paths-and-files>`_.
