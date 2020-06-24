# -*- coding: utf-8 -*-

import sys

from cli.parser import get_parser
from cli.runner import setup, generate_device_url

if __name__ == "__main__":

    ap = get_parser()
    args = ap.parse_args(sys.argv[1:])

    if args.action == 'run':
        result = setup(args.debug)
        sys.exit(0)
    elif args.action == 'gd':
        generate_device_url(args)
    else:
        ap.print_help()
