import sqlite3
import os
from xueweiinfo import XueweiInfo
from logger import Logger


class DbAgent(object):
    def __init__(self, dbfile='xueweidb.db'):
        if dbfile == 'xueweidb.db':
            data_path = os.path.join(os.path.curdir, 'data')
            db_path = os.path.join(data_path, dbfile)
        else:
            db_path = dbfile
        self.conn = sqlite3.connect(db_path)
        self.cur = self.conn.cursor()
        self.table = 'xuewei'

    def commit(self):
        self.conn.commit()

    def close(self):
        self.conn.close()

    def write_student(self, student):
        pass

    def read_student(self):
        pass

if __name__ == '__main__':
    dba = DbAgent('.\data\SEUStudents.sqlite')

