git subcommand to manage retired references
===========================================

Manage an archive of git references such as retired branches.  The
package provides the `git attic` subcommand that may be used to move
branches to the archive, to restore them, and to push and fetch the
archive to and from remote repositories.

The mechanism is to store references using a dedicated prefix that is
ignored by other git commands.  As a result, the references in the
archive are retained in the repository, but do not interfere with
daily git workflows.  The idea has been borrowed from a `reply on
Stack Overflow`__.

.. __: https://stackoverflow.com/a/41008657


.. toctree::
   :maxdepth: 2
   :caption: Contents:

   man-git-attic
   changelog


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
