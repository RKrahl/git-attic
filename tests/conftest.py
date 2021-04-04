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

def run_cmd(cmd):
    return subprocess.run(cmd,
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                          check=True, universal_newlines=True)

def git_attic(args):
    script = scriptdir / "git-attic.py"
    cmd = [sys.executable, str(script)] + list(args)
    return run_cmd(cmd)
