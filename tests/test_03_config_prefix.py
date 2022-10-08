"""Test setting the default prefix in the git config.

Similar to test_01_stash_restore.py: test list, stash and restore
subcommands of git-attic, but set another default prefix in the git
config.
"""

import pytest
from conftest import *

@pytest.fixture(scope="function")
def configured_gitrepo(gitrepo):
    cmd = ('git', '-C', str(gitrepo),
           'config', '--local', '--add', 'attic.prefix', 'barn')
    run_cmd(cmd)
    return gitrepo

def test_config_stash_and_restore_simple(monkeypatch, configured_gitrepo):
    """Stash and restore in the most simple case.
    """
    monkeypatch.chdir(configured_gitrepo)
    assert_refs(git_attic(("list", "-v")), ())
    assert_refs(git_branches(), get_test_branches())

    git_attic(("stash", "hawaii"))
    assert_refs(git_attic(("list", "-v")),
                get_test_branches(("hawaii",)))
    assert_refs(git_branches(),
                get_test_branches(("marinara", "master")))

    git_attic(("stash", "marinara"))
    assert_refs(git_attic(("list", "-v")),
                get_test_branches(("hawaii", "marinara")))
    assert_refs(git_attic(("--prefix", "barn", "list", "-v")),
                get_test_branches(("hawaii", "marinara")))
    assert_refs(git_branches(),
                get_test_branches(("master",)))
    assert set(git_attic(("list",)).stdout.split()) == {"hawaii", "marinara"}

    git_attic(("restore", "marinara"))
    assert_refs(git_attic(("list", "-v")),
                get_test_branches(("hawaii", "marinara")))
    assert_refs(git_branches(),
                get_test_branches(("marinara", "master")))

def test_config_stash_and_restore_prefix(monkeypatch, configured_gitrepo):
    """Use an alternative prefix.
    """
    monkeypatch.chdir(configured_gitrepo)
    assert_refs(git_attic(("list", "-v")), ())
    assert_refs(git_branches(), get_test_branches())

    git_attic(("--prefix", "archive", "stash", "hawaii"))
    assert_refs(git_attic(("--prefix", "archive", "list", "-v")),
                get_test_branches(("hawaii",)))
    assert_refs(git_attic(("list", "-v")), ())
    assert_refs(git_branches(),
                get_test_branches(("marinara", "master")))

    git_attic(("--prefix", "shed", "stash", "marinara"))
    assert_refs(git_attic(("--prefix", "shed", "list", "-v")),
                get_test_branches(("marinara",)))
    assert_refs(git_attic(("--prefix", "archive", "list", "-v")),
                get_test_branches(("hawaii",)))
    assert_refs(git_attic(("list", "-v")), ())
    assert_refs(git_branches(),
                get_test_branches(("master",)))
    refs = git_attic(("--prefix", "archive", "list")).stdout.split()
    assert set(refs) == {"hawaii"}

    git_attic(("--prefix", "shed", "restore", "marinara"))
    assert_refs(git_attic(("--prefix", "shed", "list", "-v")),
                get_test_branches(("marinara",)))
    assert_refs(git_branches(),
                get_test_branches(("marinara", "master")))
