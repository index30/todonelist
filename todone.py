#!/usr/local/Cellar/python3/3.5.1/bin/python3.5
import shelve
import argparse
from command import Command

db = shelve.open("data_store", "c")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('shelve')

    subparsers = parser.add_subparsers()
    add_parser = subparsers.add_parser('add')
    add_parser.set_defaults(func=Command.cmd_add)
    list_parser = subparsers.add_parser('list')
    list_parser.add_argument('-s', '--sort',
                             default="task_id")
    list_parser.set_defaults(func=Command.cmd_list)
    tag_parser = subparsers.add_parser('tag')
    tag_parser.set_defaults(func=Command.cmd_tag)
    content_parser = subparsers.add_parser('content')
    content_parser.add_argument('-c', '--change', action="store_true")
    content_parser.add_argument('-d', '--delete', action="store_true")
    content_parser.set_defaults(func=Command.cmd_content)
    args = parser.parse_args()

    db = shelve.open(args.shelve, 'c')
    try:
        args.db = db
        if hasattr(args, 'func'):
            args.func(args)
        else:
            parser.print_help()
    finally:
        db.close()

if __name__ == '__main__':
    main()



