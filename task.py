import sys
from texttable import Texttable
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import sqlite3


class Task:

    def create_task(name, content, tag, done_date, db):
        c_sql = 'select count(*) from tasks where tag = ?'
        sql = 'insert into tasks (tag_id, name, content, tag, done_date) values (?, ?, ?, ?, ?)'
        try:
            with db:
                tag_id = int(str(db.execute(c_sql, [tag]).fetchone()[0])) + 1
                task = [tag_id, name, content, tag, done_date]
                db.execute(sql, task)
        except sqlite3.IntegrityError:
            print("Couldn't add twice", file=sys.stderr)

    def update_task(db, name, content):
        sql = 'update tasks set content = ? where name = ?'
        update = [content, name]
        with db:
            db.execute(sql, update)

    def delete_task(db, name):
        sql = 'delete from tasks where name = ?'
        with db:
            db.execute(sql, [name])

    def all_task(db):
        sql = 'select * from tasks'
        table = Texttable()
        table.set_deco(Texttable.HEADER)
        table.set_cols_width([5, 6, 20, 70, 25, 30])
        table.header(['id', 'tag_id', 'タスク名', '内容', 'タグ', 'done_date'])
        table.set_cols_dtype(['i',
                              'i',
                              't',
                              't',
                              't',
                              't'])
        table.set_cols_align(["l", "l", "c", "c", "c", "c"])
        with db:
            for row in db.execute(sql):
                table.add_row(list(row))
            print(table.draw())

    def part_task(db, task_name):
        sql = 'select * from tasks where name=?'
        with db:
            if db.execute(sql, [task_name]).fetchone():
                for row in db.execute(sql, [task_name]):
                    print("task_id:{0}\ntag_id:{1}\nname:{2}\ntag:{3}\ncontent:{4}\ndone_date:{5}".format(row[0], row[1], row[2], row[4], row[3], row[5]))
                    return True
            else:
                print("This task doesn't exist", file=sys.stderr)
                return False

    def sorted_task(db, tag, sort):
        with db:
            if tag:
                if sort:
                    sql = 'select * from tasks where tag=? order by '+sort
                    ele = [tag, sort]
                    rows = db.execute(sql, ele)
                else:
                    sql = 'select * from tasks where tag=?'
                    ele = [tag]
                    rows = db.execute(sql, ele)
            else:
                if sort:
                    sql = 'select * from tasks order by '+sort
                    rows = db.execute(sql)
            table = Texttable()
            table.set_deco(Texttable.HEADER)
            table.set_cols_width([5, 6, 20, 70, 25, 30])
            table.header(['id', 'tag_id', 'タスク名', '内容', 'タグ', 'done_date'])
            table.set_cols_dtype(['i',
                                  'i',
                                  't',
                                  't',
                                  't',
                                  't'])
            table.set_cols_align(["l", "l", "c", "c", "c", "c"])
            for row in rows:
                table.add_row(list(row))
            print(table.draw())

    def print_task(db):
        with db:
            data = []
            d_num = []
            for tag, row in db.execute('select tag,count(*) from tasks group by tag'):
                data.append(tag)
                d_num.append(row)
            fig = plt.figure()
            fig.patch.set_facecolor('white')
            #colorsにcolormapを代入できない
            plt.pie(d_num, labels=data, counterclock=False, startangle=90, autopct='%1.1f%%',)
            plt.axis('equal')
            plt.show()
