from pathlib import Path
import tarfile
import pytest

testdir = Path(__file__).resolve().parent

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
