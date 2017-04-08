import sqlite3
import os
from xueweiinfo import XueweiInfo
from logger import Logger


class DbAgent(object):
    def __init__(self, dbfile='xueweidb'):
        if dbfile == 'xueweidb':
            curr_path = os.path.curdir
            db_path = os.path.join(curr_path, dbfile)
        else:
            db_path = dbfile
        self.conn = sqlite3.connect(db_path)
        self.cur = self.conn.cursor()

    def commit(self):
        self.conn.commit()

    def close(self):
        self.conn.close()

    def write_student(self, student):
        pass

if __name__ == '__main__':
    pass