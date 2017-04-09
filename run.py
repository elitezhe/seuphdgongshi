import multiprocessing as mp
import queue
import time
from config import config
from logger import Logger
from xueweiinfo import XueweiInfo
from dbagent import DbAgent
from agent import Agent


if __name__ == '__main__':
    Logger.info('程序开始')
    inqueue = mp.Manager().Queue()
    outqueue = mp.Manager().Queue()

    start_time = time.time()  # 开始时间

    dba = DbAgent(outqueue, config['db_path'])
    un_list = dba.get_uncrawled_student_list()
    for item in un_list:
        inqueue.put(XueweiInfo(item))
    inqueue.put(XueweiInfo('-1'))  # 队列末尾两个-1, 可能出错

    num_threads = config['num_threads']
    p = []
    for i in range(num_threads):
        agent = Agent(inqueue, outqueue)
        # print(agent)
        p.append(mp.Process(target=agent.run, args=()))
        p[i].start()



    for i in range(num_threads):
        p[i].join()
    Logger.info('数据抓取完成')
    #  生产者agent进程完成,想办法释放dbagent
    outqueue.put(XueweiInfo('-1'))

    dba.run()  # 开启数据库agent进程
    # 以下代码不正确, sqlite3不能pickle,所以不能开进程
    # p_dba = mp.Process(target=dba.run, args=())
    # p_dba.start()
    # p_dba.join()

    dba.commit()
    dba.close()

    end_time = time.time()  #结束时间
    Logger.debug("程序运行耗时 %f" % (end_time - start_time))
