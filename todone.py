#!/usr/local/Cellar/python3/3.5.1/bin/python3.5
from datetime import datetime, time
import pickle
import shelve
import sys
import argparse

db = shelve.open("data_store", "c")

def create_task(name, content, tag):
    return dict(name=name, content=content, tag=tag)

def format_task(task):
    format = "{task[tag]}: {task[name]}: {task[content]}"
    return format.format(task=task)

def update_task(task, content):
    task['content'] = content

def next_task_name(db):
    id = db.get('next_id', 0)
    db['next_id'] = id + 1
    return "task:{0}".format(id)

def add_task(db, task):
    key = next_task_name(db)
    db[key] = task

def all_task(db):
    for key in db:
        if key.startswith('task:'):
            yield key, db[key]

def tag_task(db, tag):
    return((key, task)
           for key, task in all_task(db)
           if task['tag'] == tag
    )

def cmd_add(args):
    name = input('task name:')
    content = input('task content:')
    tag = input('task\'s tag:')
    task = create_task(name, content, tag)
    add_task(args.db, task)

def cmd_list(args):
    tasks = all_task(args.db)
    for key, task in tasks:
        print("{0} {1}".format(key, format_task(task)))

def cmd_tag(args):
    tag = input('tag:')
    tasks = tag_task(args.db, tag)
    for key, task in tasks:
        print("{0} {1}".format(key, format_task(task)))

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('shelve')

    subparsers = parser.add_subparsers()
    add_parser = subparsers.add_parser('add')
    add_parser.set_defaults(func=cmd_add)
    list_parser = subparsers.add_parser('list')
    list_parser.add_argument('-a', '--all', action="store_true")
    list_parser.set_defaults(func=cmd_list)
    tag_parser = subparsers.add_parser('tag')
    tag_parser.set_defaults(func=cmd_tag)

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


