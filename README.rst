.. image:: https://github.com/ome/omero-cli-duplicate/workflows/OMERO/badge.svg
    :target: https://github.com/ome/omero-cli-duplicate/actions

.. image:: https://badge.fury.io/py/omero-cli-duplicate.svg
    :target: https://badge.fury.io/py/omero-cli-duplicate

omero-cli-duplicate
===================

OMERO command-line plugin for duplicating Objects in OMERO, without duplicating binary data.

For usage instructions, please see `OMERO guides <https://omero-guides.readthedocs.io/projects/introduction/en/latest/data-management.html?#command-line-duplicating-objects>`_.


Requirements
============

* OMERO 5.6.0 or newer
* Python 3.6 or newer


Installing from PyPI
====================

This section assumes that an OMERO.py is already installed.

Install the command-line tool using `pip <https://pip.pypa.io/en/stable/>`_:

::

    $ pip install -U omero-cli-duplicate

Release process
---------------

This repository uses `bump2version <https://pypi.org/project/bump2version/>`_ to manage version numbers.
To tag a release run::

    $ bumpversion release

This will remove the ``.dev0`` suffix from the current version, commit, and tag the release.

To switch back to a development version run::

    $ bumpversion --no-tag [major|minor|patch]

specifying ``major``, ``minor`` or ``patch`` depending on whether the development branch will be a `major, minor or patch release <https://semver.org/>`_. This will also add the ``.dev0`` suffix.

Remember to ``git push`` all commits and tags.

License
-------

This project, similar to many Open Microscopy Environment (OME) projects, is
licensed under the terms of the GNU General Public License (GPL) v2 or later.

Copyright
---------

2017-2020, The Open Microscopy Environment
