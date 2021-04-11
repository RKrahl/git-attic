#! python

import argparse
import subprocess
import sys


def _rungit(cmd):
    kwargs = dict(stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                  check=True, universal_newlines=True)
    return subprocess.run(cmd, **kwargs)

def listrefs(args):
    prefix = 'refs/%s/' % args.prefix
    if args.verbose:
        fmt = '%(refname:lstrip=2) %(objectname:short) %(contents:subject)'
    else:
        fmt = '%(refname:lstrip=2)'
    proc = _rungit(('git', 'for-each-ref', '--format=%s' % fmt, prefix))
    if args.verbose:
        maxlen = 0
        reftuples = []
        for l in proc.stdout.splitlines():
            r, c, s = l.split(' ', maxsplit=2)
            maxlen = max(maxlen, len(r))
            reftuples.append((r, c, s))
        f = "%%-%ds   %%s   %%s" % maxlen
        for t in reftuples:
            print(f % t)
    else:
        print(proc.stdout, end="")


def stash(args):
    branch = args.branch
    archref = 'refs/%s/%s' % (args.prefix, args.archivename or args.branch)
    _rungit(('git', 'update-ref', archref, branch, ""))
    _rungit(('git', 'branch', '-D', branch))


def restore(args):
    branch = args.branch or args.archivename
    archref = 'refs/%s/%s' % (args.prefix, args.archivename)
    _rungit(('git', 'branch', branch, archref))


def push(args):
    refspec = 'refs/%s/*:refs/%s/*' % (args.prefix, args.prefix)
    remote = args.remote
    if args.verbose:
        _rungit(('git', 'push', '-v', remote, refspec))
    else:
        _rungit(('git', 'push', remote, refspec))


def fetch(args):
    refspec = 'refs/%s/*:refs/%s/*' % (args.prefix, args.prefix)
    remote = args.remote
    if args.verbose:
        _rungit(('git', 'fetch', '-v', remote, refspec))
    else:
        _rungit(('git', 'fetch', remote, refspec))


def main():
    description = "Manage an archive of retired references"
    argparser = argparse.ArgumentParser(description=description)
    argparser.add_argument('--prefix', default="attic", help="archive prefix")
    argparser.add_argument('-v', action='store_true', dest='verbose',
                           help="verbose list")
    subparsers = argparser.add_subparsers(title='subcommands', dest='subcmd')
    listparser = subparsers.add_parser('list', help="list references")
    listparser.set_defaults(func=listrefs)
    stashparser = subparsers.add_parser('stash', help="move a branch "
                                        "to the archive")
    stashparser.add_argument('branch')
    stashparser.add_argument('archivename', nargs='?')
    stashparser.set_defaults(func=stash)
    restoreparser = subparsers.add_parser('restore', help="restore a branch "
                                          "from the archive")
    restoreparser.add_argument('archivename')
    restoreparser.add_argument('branch', nargs='?')
    restoreparser.set_defaults(func=restore)
    pushparser = subparsers.add_parser('push', help="push archive to "
                                       "remote repository")
    pushparser.add_argument('remote')
    pushparser.set_defaults(func=push)
    fetchparser = subparsers.add_parser('fetch', help="fetch archive from "
                                        "remote repository")
    fetchparser.add_argument('remote')
    fetchparser.set_defaults(func=fetch)
    args = argparser.parse_args()
    getattr(args, 'func', listrefs)(args)


if __name__ == "__main__":
    try:
        main()
    except subprocess.CalledProcessError as e:
        print(e.stderr, end='', file=sys.stderr)
        sys.exit(e.returncode)
