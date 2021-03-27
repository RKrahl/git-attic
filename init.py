#! python3

import argparse
from pathlib import Path
import string
import subprocess


argparser = argparse.ArgumentParser(description="Initialize the repository.")
argparser.add_argument("distname", help="name of the package")
args = argparser.parse_args()


tagmsg = """Tag initial commit.  This is not a release version.

Add this tag solely to make sure there is a tag somewhere in the
history that looks like a version number.
"""
subprocess.check_call(["git", "tag", "-a", "-m", tagmsg, "0.0"])


distname_files = (
    Path(".gitignore"),
    Path("Makefile"),
    Path("doc/Makefile"),
    Path("doc/src/conf.py"),
    Path("doc/src/index.rst"),
    Path("python-skel.spec"),
    Path("setup.py"),
    Path("tests/test_00.py"),
)

for path in distname_files:
    with path.open("rt") as f:
        s = string.Template(f.read())
    with path.open("wt") as f:
        f.write(s.safe_substitute(distname=args.distname))
    subprocess.check_call(["git", "add", str(path)])

subprocess.check_call(["git", "mv",
                       "python-skel.spec", "python-%s.spec" % args.distname])
subprocess.check_call(["git", "rm", "init.py"])
subprocess.check_call(["git", "commit", "-m", "Set the name of the package."])

print("""Name of the package set.

Next steps: fix the url in setup.py and adapt the description of the
package in the doc string in setup.py and in the README.rst.

Also have a look into the documentation sources in doc/src""")
