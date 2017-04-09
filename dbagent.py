import sqlite3
import os
import multiprocessing as mp
import queue
import time
from xueweiinfo import XueweiInfo
from logger import Logger


class DbAgent(object):
    def __init__(self, inqueue, dbfile='xueweidb.db'):
        if dbfile == 'xueweidb.db':
            data_path = os.path.join(os.path.curdir, 'data')
            db_path = os.path.join(data_path, dbfile)
        else:
            db_path = dbfile
        self.conn = sqlite3.connect(db_path)
        self.cur = self.conn.cursor()
        self.table = 'xuewei'
        self.i_queue = inqueue

    def commit(self):
        self.conn.commit()

    def close(self):
        self.conn.close()

    def get_uncrawled_student_list(self):
        """返回学号(string)的列表 -- list(string)"""
        sql = r'SELECT XH FROM xuewei WHERE HAVEDATA == 0'
        self.cur.execute(sql)
        result = self.cur.fetchall()
        stu_list = []
        if len(result) > 0:
            for res in result:
                stu_list.append(res[0])
            stu_list.append('-1')
            return stu_list
        else:
            return ['-1']

    def write_student(self, student):
        xh = student.get_xh()
        if xh == '-1':
            return
        sql = student.save_to_database()
        self.cur.execute(sql)

        student.pickle_dump()  # pickle存入data文件夹

        sql2 = "UPDATE xuewei SET HAVEDATA = 1 WHERE XH = '%s'" % xh
        self.cur.execute(sql2)

    def read_student(self):
        pass

    def run(self):
        while True:
            if not self.i_queue.empty():
                try:
                    now = self.i_queue.get()
                    if now.get_xh() == '-1':
                        return  # 进程停止
                    self.write_student(now)
                except queue.Empty:
                    time.sleep(2)  # 队列空,等待若干秒
                    continue


if __name__ == '__main__':
    inqueue = mp.Manager().Queue()
    dba = DbAgent(inqueue, '.\data\SEUStudents.sqlite')
    stu_list = dba.get_uncrawled_student_list()
    print(stu_list)

