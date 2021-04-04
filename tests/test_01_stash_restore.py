"""Test list, stash and restore subcommands of git-attic.
"""

import pytest
from conftest import get_test_branches, git_attic, git_branches, assert_refs

def test_stash_and_restore_simple(monkeypatch, gitrepo):
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
