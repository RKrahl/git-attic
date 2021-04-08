"""Test list, stash and restore subcommands of git-attic.
"""

import pytest
from conftest import get_test_branches, git_attic, git_branches, assert_refs

def test_stash_and_restore_simple(monkeypatch, gitrepo):
    """Stash and restore in the most simple case.
    """
    monkeypatch.chdir(gitrepo)
    assert_refs(git_attic(("-v", "list")), ())
    assert_refs(git_branches(), get_test_branches())

    git_attic(("stash", "hawaii"))
    assert_refs(git_attic(("-v", "list")),
                get_test_branches(("hawaii",)))
    assert_refs(git_branches(),
                get_test_branches(("marinara", "master")))

    git_attic(("stash", "marinara"))
    assert_refs(git_attic(("-v", "list")),
                get_test_branches(("hawaii", "marinara")))
    assert_refs(git_branches(),
                get_test_branches(("master",)))
    assert set(git_attic(("list",)).stdout.split()) == {"hawaii", "marinara"}

    git_attic(("restore", "marinara"))
    assert_refs(git_attic(("-v", "list")),
                get_test_branches(("hawaii", "marinara")))
    assert_refs(git_branches(),
                get_test_branches(("marinara", "master")))

def test_stash_and_restore_prefix(monkeypatch, gitrepo):
    """Use an alternative prefix.
    """
    monkeypatch.chdir(gitrepo)
    assert_refs(git_attic(("-v", "list")), ())
    assert_refs(git_branches(), get_test_branches())

    git_attic(("--prefix", "archive", "stash", "hawaii"))
    assert_refs(git_attic(("--prefix", "archive", "-v", "list")),
                get_test_branches(("hawaii",)))
    assert_refs(git_attic(("-v", "list")), ())
    assert_refs(git_branches(),
                get_test_branches(("marinara", "master")))

    git_attic(("--prefix", "shed", "stash", "marinara"))
    assert_refs(git_attic(("--prefix", "shed", "-v", "list")),
                get_test_branches(("marinara",)))
    assert_refs(git_attic(("--prefix", "archive", "-v", "list")),
                get_test_branches(("hawaii",)))
    assert_refs(git_attic(("-v", "list")), ())
    assert_refs(git_branches(),
                get_test_branches(("master",)))
    refs = git_attic(("--prefix", "archive", "list")).stdout.split()
    assert set(refs) == {"hawaii"}

    git_attic(("--prefix", "shed", "restore", "marinara"))
    assert_refs(git_attic(("--prefix", "shed", "-v", "list")),
                get_test_branches(("marinara",)))
    assert_refs(git_branches(),
                get_test_branches(("marinara", "master")))

def test_stash_and_restore_rename(monkeypatch, gitrepo):
    """Stash and restore refs using a different name.
    """
    monkeypatch.chdir(gitrepo)
    assert_refs(git_attic(("-v", "list")), ())
    assert_refs(git_branches(), get_test_branches())

    git_attic(("stash", "hawaii", "a1"))
    assert_refs(git_attic(("-v", "list")),
                get_test_branches((("hawaii", "a1"),)))
    assert_refs(git_branches(),
                get_test_branches(("marinara", "master")))

    git_attic(("stash", "marinara", "a2"))
    assert_refs(git_attic(("-v", "list")),
                get_test_branches((("hawaii", "a1"), ("marinara", "a2"))))
    assert_refs(git_branches(),
                get_test_branches(("master",)))
    assert set(git_attic(("list",)).stdout.split()) == {"a1", "a2"}

    git_attic(("restore", "a2", "b2"))
    assert_refs(git_attic(("-v", "list")),
                get_test_branches((("hawaii", "a1"), ("marinara", "a2"))))
    assert_refs(git_branches(),
                get_test_branches((("marinara", "b2"), "master")))
