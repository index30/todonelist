#!/usr/local/Cellar/python3/3.5.1/bin/python3.5
from datetime import datetime, time
import pickle
import shelve
import sys
import argparse
from operator import itemgetter

db = shelve.open("data_store", "c")


def create_task(name, content, tag, done_date, db):
    task_id = db.get('next_id', 0)
    tag_id = db.get(tag, 0)
    task_key = "task:{0}".format(task_id)
    db['next_id'] = task_id + 1
    db[tag] = tag_id + 1
    task = dict(name=name, content=content, tag=tag,
                done_date=done_date, task_id=task_id, tag_id=tag_id)
    db[task_key] = task


def format_task(task):
    format = "{task[tag]}: {task[name]}: {task[done_date]}"
    return format.format(task=task)


def format_content(task):
    format = "tag:{task[tag]}\n name:{task[name]}:\n content:{task[content]}\n date:{task[done_date]}"
    return format.format(task=task)


def update_task(task, content):
    task['content'] = content

def delete_task(db, task):
    task_key = "task:{0}".format(task['task_id'])
    task_id = db.get('next_id', 0)
    tag_id = db.get(task['tag'], 0)
    del db[task_key]
    #db['next_id'] = task_id - 1
    #db[task['tag']] = tag_id - 1


def all_task(db):
    for key in db:
        if key.startswith('task:'):
            yield key, db[key]


def part_task(db, task_name):
    for key in db:
        if key.startswith('task:') and db[key]['name'] == task_name:
            yield key, db[key]


def tag_task(db, tag):
    return(sorted(
        (key, task)
        for key, task in all_task(db)
        if task['tag'] == tag
    )
    )


def cmd_add(args):
    name = input('task name:')
    content = input('task content:')
    tag = input('task\'s tag:')
    done_date = datetime.strptime(input('done date [Y-m]:'), '%Y-%m')
    task = create_task(name, content, tag, done_date, args.db)


def cmd_list(args):
    tasks = all_task(args.db)

    if args.sort:
        sort_task = args.sort
    else:
        sort_task = 'task_id'

    for key, task in sorted(tasks, key=lambda x: x[1][sort_task]):
        print("{0}".format(format_task(task)))


def cmd_tag(args):
    tag = input('tag:')
    tasks = tag_task(args.db, tag)
    for key, task in tasks:
        print("{0}".format(format_task(task)))


def cmd_content(args):
    task_name = input('task_name:')
    task = part_task(args.db, task_name)
    for key, t in task:
        if args.delete:
            delete_task(args.db, t)
            print("Delete task:{0}",task_name)
        else:
            if args.change:
                content = input('content:')
                update_task(t,content)
                task = part_task(args.db, task_name)
            print("{0}".format(format_content(t)))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('shelve')

    subparsers = parser.add_subparsers()
    add_parser = subparsers.add_parser('add')
    add_parser.set_defaults(func=cmd_add)
    list_parser = subparsers.add_parser('list')
    list_parser.add_argument('-s', '--sort',
                             default="task_id")
    list_parser.set_defaults(func=cmd_list)
    tag_parser = subparsers.add_parser('tag')
    tag_parser.set_defaults(func=cmd_tag)
    content_parser = subparsers.add_parser('content')
    content_parser.add_argument('-c', '--change', action="store_true")
    content_parser.add_argument('-d', '--delete', action="store_true")
    content_parser.set_defaults(func=cmd_content)
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


