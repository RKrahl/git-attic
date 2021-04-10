import os
from pathlib import Path
import subprocess
import sys
import tarfile
import pytest

testdir = Path(__file__).resolve().parent
try:
    scriptdir = Path(os.environ['BUILD_SCRIPTS_DIR'])
except KeyError:
    raise RuntimeError("script directory not set, "
                       "please use 'setup.py test'") from None

def gettestdata(fname):
    fname = testdir / "data" / fname
    assert fname.is_file()
    return fname

@pytest.fixture(scope="function")
def gitrepo(tmp_path):
    try:
        with tarfile.open(str(gettestdata("repo.tar.xz"))) as tar:
            tar.extractall(path=str(tmp_path))
    except tarfile.CompressionError as err:
        pytest.skip(str(err))
    return tmp_path / "repo"

# The branches present in the test git repo
_test_branches = {
    'hawaii':   ('hawaii',     '94ef0ab',   'Esst mehr Obst!'),
    'marinara': ('marinara',   'fa5b55e',   'Jetzt neu: Marinara'),
    'master':   ('master',     '455d80c',   'Zubereitung'),
}
def get_test_branches(names='*'):
    """Get a selection of the branches present in the test data.
    """
    if names == '*':
        return set(_test_branches.values())
    else:
        refs = set()
        for n in names:
            if isinstance(n, str):
                refs.add(_test_branches[n])
            else:
                refs.add((n[1],) + _test_branches[n[0]][1:])
        return refs


def run_cmd(cmd):
    """Run a command, capturing the output.

    Note: with Python 3.7 we could simplify this using
    (check=True, capture_output=True, text=True).
    """
    return subprocess.run(cmd,
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                          check=True, universal_newlines=True)

def git_attic(args):
    """Call the git-attic script.
    """
    script = scriptdir / "git-attic.py"
    cmd = [sys.executable, str(script)] + list(args)
    return run_cmd(cmd)

def git_branches():
    """Call git branch to get the branches from the current repository.
    """
    fmt = '%(refname:lstrip=2) %(objectname:short) %(contents:subject)'
    cmd = ('git', 'branch', '--format=%s' % fmt)
    return run_cmd(cmd)

def assert_refs(proc, refs):
    """Assert that the stdout of proc is a given list of refs.
    """
    outrefs = { tuple(l.split(maxsplit=2)) for l in proc.stdout.splitlines() }
    assert outrefs == set(refs)
