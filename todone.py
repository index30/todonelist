#!/usr/local/Cellar/python3/3.5.1/bin/python3.5
import argparse
import sqlite3
from command import Command

db_name = "d_todone.db"


def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()
    add_parser = subparsers.add_parser('add')
    add_parser.set_defaults(func=Command.cmd_add)
    list_parser = subparsers.add_parser('list')
    list_parser.add_argument('-t', '--tag')
    list_parser.add_argument('-s', '--sort',
                             default="id")
    list_parser.add_argument('-p', '--print', action="store_true")
    list_parser.set_defaults(func=Command.cmd_list)
    content_parser = subparsers.add_parser('content')
    content_parser.add_argument('-c', '--change', action="store_true")
    content_parser.add_argument('-d', '--delete', action="store_true")
    content_parser.set_defaults(func=Command.cmd_content)
    args = parser.parse_args()
    args.db = sqlite3.connect(db_name)
    if hasattr(args, 'func'):
        args.func(args)
    else:
        parser.print_help()

if __name__ == '__main__':
    main()
