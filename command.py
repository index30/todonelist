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
            tasks = Task.all_task(args.db)
        else:
            tasks = Task.tag_task(args.db, args.tag)
        if args.sort:
            sort_task = args.sort
        else:
            sort_task = 'task_id'
        for key, task in sorted(tasks, key=lambda x: x[1][sort_task]):
            print("{0}".format(Task.format_task(task)))

    def cmd_content(args):
        task_name = input('task_name:')
        task = Task.part_task(args.db, task_name)
        for key, t in task:
            if args.delete:
                Task.delete_task(args.db, t)
                print("Delete task:{0}",task_name)
            else:
                if args.change:
                    content = input('content:')
                    Task.update_task(t, content)
                    task = Task.part_task(args.db, task_name)
                print("{0}".format(Task.format_content(t)))
