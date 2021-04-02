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
        f_arg = '--format=%(refname) %(objectname:short) %(contents:subject)'
    else:
        f_arg = '--format=%(refname)'
    proc = _rungit(('git', 'for-each-ref', f_arg, prefix))
    reflines = proc.stdout.splitlines()
    if args.verbose:
        maxlen = 0
        reftuples = []
        for l in reflines:
            r, c, s = l.split(' ', maxsplit=2)
            assert r.startswith(prefix)
            r = r[len(prefix):]
            maxlen = max(maxlen, len(r))
            reftuples.append((r, c, s))
        f = "%%-%ds   %%s   %%s" % maxlen
        for t in reftuples:
            print(f % t)
    else:
        for l in reflines:
            assert l.startswith(prefix)
            print(l[len(prefix):])


def main():
    description = "Manage an archive of retired references"
    argparser = argparse.ArgumentParser(description=description)
    argparser.add_argument('--prefix', default="attic", help="archive prefix")
    argparser.add_argument('-v', action='store_true', dest='verbose',
                           help="verbose list")
    subparsers = argparser.add_subparsers(title='subcommands', dest='subcmd')
    listparser = subparsers.add_parser('list', help="list references")
    listparser.set_defaults(func=listrefs)
    args = argparser.parse_args()
    getattr(args, 'func', listrefs)(args)


if __name__ == "__main__":
    try:
        main()
    except subprocess.CalledProcessError as e:
        print(e.stderr, end='', file=sys.stderr)
        sys.exit(e.returncode)
