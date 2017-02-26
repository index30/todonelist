from datetime import datetime
from task import Task


class Command:
    def cmd_add(args):
        name = input('task name:')
        content = input('task content:')
        tag = input('task\'s tag:')
        done_date = datetime.strptime(input('done date [Y-m]:'), '%Y-%m')
        Task.create_task(name, content, tag, done_date, args.db)

    def cmd_list(args):
        if args.tag is None:
            Task.all_task(args.db)
        else:
            Task.tag_task(args.db, args.tag)
        #if args.sort:
        #    sort_task = args.sort
        #else:
        #    sort_task = 'task_id'

    def cmd_content(args):
        task_name = input('task_name:')
        if args.delete:
            Task.delete_task(args.db, task_name)
            print("Delete task:{0}", task_name)
        else:
            Task.part_task(args.db, task_name)
            if args.change:
                content = input('content:')
                Task.update_task(args.db, task_name, content)
                Task.part_task(args.db, task_name)
