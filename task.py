class Task:

    def create_task(name, content, tag, done_date, db):
        cur = db.cursor()
        c_sql = 'select count(*) from tasks where tag = ?'
        sql = 'insert into tasks (tag_id, name, content, tag, done_date) values (?, ?, ?, ?, ?)'
        tag_id = int(str(cur.execute(c_sql, [tag]).fetchone()[0]))
        task = (tag_id, name, content, tag, done_date)
        cur.execute(sql, task)
        db.commit()
        db.close()

    def update_task(db, name, content):
        sql = 'update tasks set content = ? where name = ?'
        update = [content, name]
        db.execute(sql, update)
        db.commit()
        db.close()

    def delete_task(db, name):
        cur = db.cursor()
        sql = 'delete from tasks where name = ?'
        cur.execute(sql, [name])
        db.commit()
        db.close()

    def all_task(db):
        cur = db.cursor()
        sql = 'select * from tasks'
        for row in cur.execute(sql):
            print(row[4])
        db.close()

    def part_task(db, task_name):
        sql = 'select * from tasks where name=?'
        for key in db.execute(sql, task_name):
            print("tag: {row[4]}\n name: {row[2]}\n content: {row[3]}\n done_date: {row[5]}")

    def tag_task(db, tag):
        sql = 'select * from tasks where tag=?'
        for row in db.execute(sql, tag):
            print("{row[4]}...{row[2]} <date>:{row[5]}")
