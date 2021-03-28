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


System requirements
-------------------

Python:

+ Python 3.4 or newer.

External Programs:

+ `git`_.

Required library packages:

+ None

Optional library packages:

+ `setuptools_scm`_

  The version number is managed using this package.  All source
  distributions add a static text file with the version number and
  fall back using that if `setuptools_scm` is not available.  So this
  package is only needed to build out of the plain development source
  tree as cloned from GitHub.

+ `pytest`_ >= 3.0

  Only needed to run the test suite.

+ `distutils-pytest`_

  Only needed to run the test suite.


Copyright and License
---------------------

Copyright 2021 Rolf Krahl

Licensed under the `Apache License`_, Version 2.0 (the "License"); you
may not use this file except in compliance with the License.

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
implied.  See the License for the specific language governing
permissions and limitations under the License.


.. _git: https://git-scm.com/
.. _setuptools_scm: https://github.com/pypa/setuptools_scm/
.. _pytest: https://pytest.org/
.. _distutils-pytest: https://github.com/RKrahl/distutils-pytest
.. _Apache License: https://www.apache.org/licenses/LICENSE-2.0
