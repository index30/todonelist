class Task:

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
