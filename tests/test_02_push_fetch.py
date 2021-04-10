"""Test push and fetch subcommands of git-attic.
"""

import pytest
from conftest import *

def test_fetch_simple(monkeypatch, gitrepo):
    """Fetch the attic refs in the most simple case.
    """
    monkeypatch.chdir(gitrepo)
    git_attic(("stash", "hawaii"))
    git_attic(("stash", "marinara"))

    monkeypatch.chdir(clone_repo(gitrepo))
    assert_refs(git_attic(("-v", "list")), ())
    assert_refs(git_branches(), get_test_branches(("master",)))
    git_attic(("fetch", "origin"))
    assert_refs(git_attic(("-v", "list")),
                get_test_branches(("hawaii", "marinara")))

def test_fetch_prefix(monkeypatch, gitrepo):
    """Fetch with an alternative prefix.
    """
    monkeypatch.chdir(gitrepo)
    git_attic(("stash", "hawaii"))
    git_attic(("--prefix", "archive", "stash", "marinara"))

    monkeypatch.chdir(clone_repo(gitrepo))
    assert_refs(git_attic(("-v", "list")), ())
    assert_refs(git_branches(), get_test_branches(("master",)))
    git_attic(("fetch", "origin"))
    assert_refs(git_attic(("-v", "list")),
                get_test_branches(("hawaii",)))
    assert_refs(git_attic(("--prefix", "archive", "-v", "list")), ())
    git_attic(("--prefix", "archive", "fetch", "origin"))
    assert_refs(git_attic(("-v", "list")),
                get_test_branches(("hawaii",)))
    assert_refs(git_attic(("--prefix", "archive", "-v", "list")),
                get_test_branches(("marinara",)))

def test_push_simple(monkeypatch, gitrepo):
    """Push the attic refs in the most simple case.
    """
    monkeypatch.chdir(gitrepo)
    assert_refs(git_attic(("-v", "list")), ())

    monkeypatch.chdir(clone_repo(gitrepo))
    cmd = ('git', 'branch', 'hawaii', '--track', 'origin/hawaii')
    run_cmd(cmd)
    cmd = ('git', 'branch', 'marinara', '--track', 'origin/marinara')
    run_cmd(cmd)
    git_attic(("stash", "hawaii"))
    git_attic(("stash", "marinara"))
    assert_refs(git_attic(("-v", "list")),
                get_test_branches(("hawaii", "marinara")))
    assert_refs(git_branches(), get_test_branches(("master",)))
    git_attic(("push", "origin"))

    monkeypatch.chdir(gitrepo)
    assert_refs(git_attic(("-v", "list")),
                get_test_branches(("hawaii", "marinara")))

def test_push_prefix(monkeypatch, gitrepo):
    """Push with an alternative prefix.
    """
    monkeypatch.chdir(gitrepo)
    assert_refs(git_attic(("-v", "list")), ())

    clone = clone_repo(gitrepo)
    monkeypatch.chdir(clone)
    cmd = ('git', 'branch', 'hawaii', '--track', 'origin/hawaii')
    run_cmd(cmd)
    cmd = ('git', 'branch', 'marinara', '--track', 'origin/marinara')
    run_cmd(cmd)
    git_attic(("stash", "hawaii"))
    git_attic(("--prefix", "archive", "stash", "marinara"))
    assert_refs(git_attic(("-v", "list")),
                get_test_branches(("hawaii",)))
    assert_refs(git_attic(("--prefix", "archive", "-v", "list")),
                get_test_branches(("marinara",)))
    assert_refs(git_branches(), get_test_branches(("master",)))
    git_attic(("push", "origin"))

    monkeypatch.chdir(gitrepo)
    assert_refs(git_attic(("-v", "list")),
                get_test_branches(("hawaii",)))
    assert_refs(git_attic(("--prefix", "archive", "-v", "list")), ())

    monkeypatch.chdir(clone)
    git_attic(("--prefix", "archive", "push", "origin"))

    monkeypatch.chdir(gitrepo)
    assert_refs(git_attic(("-v", "list")),
                get_test_branches(("hawaii",)))
    assert_refs(git_attic(("--prefix", "archive", "-v", "list")),
                get_test_branches(("marinara",)))
