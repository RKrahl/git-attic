"""git subcommand to manage retired references

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
"""

import distutils.cmd
import distutils.command.build_py
import distutils.command.sdist
from distutils.core import setup
import distutils.log
from glob import glob
from pathlib import Path
import string
try:
    import distutils_pytest
except ImportError:
    pass
try:
    import setuptools_scm
    version = setuptools_scm.get_version()
except (ImportError, LookupError):
    try:
        import _meta
        version = _meta.__version__
    except ImportError:
        distutils.log.warn("warning: cannot determine version number")
        version = "UNKNOWN"

doclines = __doc__.strip().split("\n")


class meta(distutils.cmd.Command):

    description = "generate a _meta.py file"
    user_options = []
    meta_template = '''
__version__ = "%(version)s"
'''

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        values = {
            'version': self.distribution.get_version(),
        }
        with open("_meta.py", "wt") as f:
            print(self.meta_template % values, file=f)


class sdist(distutils.command.sdist.sdist):
    def run(self):
        self.run_command('meta')
        super().run()
        subst = {
            "version": self.distribution.get_version(),
            "url": self.distribution.get_url(),
            "description": self.distribution.get_description(),
            "long_description": self.distribution.get_long_description(),
        }
        for spec in glob("*.spec"):
            with Path(spec).open('rt') as inf:
                with Path(self.dist_dir, spec).open('wt') as outf:
                    outf.write(string.Template(inf.read()).substitute(subst))


setup(
    name = "git-attic",
    version = version,
    description = doclines[0],
    long_description = "\n".join(doclines[2:]),
    author = "Rolf Krahl",
    author_email = "rolf@rotkraut.de",
    url = "https://github.com/RKrahl/git-attic",
    license = "Apache-2.0",
    requires = [],
    scripts = ["scripts/git-attic.py"],
    classifiers = [
        "Development Status :: 1 - Planning",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: Software Development :: Version Control :: Git",
    ],
    cmdclass = {'sdist': sdist, 'meta': meta},
)

