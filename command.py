from datetime import datetime
from task import Task
from logging import getLogger, StreamHandler, DEBUG
logger = getLogger(__name__)
handler = StreamHandler()
handler.setLevel(DEBUG)
logger.setLevel(DEBUG)
logger.addHandler(handler)


class Command:
    def cmd_add(args):
        name = input('task name:')
        content = input('task content:')
        tag = input('task\'s tag:')
        done_date = datetime.strptime(input('done date [Y-m]:'), '%Y-%m')
        Task.create_task(name, content, tag, done_date, args.db)
        logger.info("Create task:{0}".format(name))

    def cmd_list(args):
        if args.print:
            Task.print_task(args.db)
        if args.tag or args.sort:
            Task.sorted_task(args.db, args.tag, args.sort)
        else:
            Task.all_task(args.db)

    def cmd_content(args):
        task_name = input('please input task\'s name:')
        b_exist = Task.part_task(args.db, task_name)
        if args.delete and b_exist:
            Task.delete_task(args.db, task_name)
            logger.info("Delete task:{0}".format(task_name))
        elif args.change and b_exist:
            content = input('content:')
            Task.update_task(args.db, task_name, content)
            logger.info("Update task:{0}".format(task_name))
