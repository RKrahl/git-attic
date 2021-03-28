git-attic
=========


Synopsis
~~~~~~~~

- *git attic* [--prefix <prefix>] [list] [-v]
- *git attic* [--prefix <prefix>] stash <branch> [<archivename>]
- *git attic* [--prefix <prefix>] restore <archivename> [<branch>]
- *git attic* [--prefix <prefix>] push <remote>
- *git attic* [--prefix <prefix>] fetch <remote>


Description
~~~~~~~~~~~

Manage an archive of git references such as retired branches.  Use
**git attic** to move branches to the archive, to restore them, and to
push and fetch the archive to and from remote repositories.


Commands
~~~~~~~~

.. program:: git-attic

.. option:: list [-v]

    List references in the archive.

.. option:: stash <branch> [<archivename>]

    Move a branch to the archive.  Create a new reference named
    `<archivename>` in the archive to point to the head of branch
    `<branch>` and delete that branch.  If the `<archivename>`
    argument is ommitted, `<branch>` will be used.

.. option:: restore <archivename> [<branch>]

    Restore a branch from tha archive.  Create a branch `<branch` and
    set its head to the reference `<archivename>` in the archive.  If
    the `<branch>` argument is ommitted, `<archivename>` will be used
    for the name of the new branch.

.. option:: push <remote>

    Push all references in the archive to the remote repository
    `<remote>`.

.. option:: fetch <remote>

    Fetch all references from the archive in the remote repository
    `<remote>`.


Options
~~~~~~~

.. program:: git-attic

.. option:: --prefix <prefix>

    Set the prefix for the references in the archive.

.. option:: -v

    When used with list, show sha1 and commit subject line for each
    head.


See also
~~~~~~~~

.. only:: man

    :manpage:`git-update-ref(1)`
