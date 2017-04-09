import multiprocessing as mp
import queue
import os
import time
from xueweiinfo import XueweiInfo
from logger import Logger


class Agent():
    def __init__(self, inqueue, outqueue):
        self.i_queue = inqueue
        self.o_queue = outqueue
        self.now = XueweiInfo('0')

    def crawl(self):
        # pid = os.getpid()
        # Logger.info("Pid: %d  processing  %s; %s" % (pid, self.now.get_xh(), self))
        # time.sleep(2)
        Logger.info("Now crawl student: %s" % self.now.get_xh())
        self.now.get_raw()
        try:
            self.now.translate_raw()
            self.o_queue.put(self.now)
        except:  # 信息为空
            Logger.info("%s 无信息" % self.now.get_xh())

    def run(self):
        while True:
            if not self.i_queue.empty():
                try:
                    self.now = self.i_queue.get()
                    # 用StopFlag退出运行(return)
                    # StopFlag应是从队列中获取的,由于多线程运行,获取到StopFlag后,还应put另外一个StopFlag到队列中
                    if self.now.get_xh() == '-1':
                        self.i_queue.put(XueweiInfo('-1'))
                        return
                except queue.Empty:
                    time.sleep(2)  # 队列空,等待若干秒
                    continue

                self.crawl()


if __name__ == '__main__':
    Logger.info('程序开始')

    inqueue = mp.Manager().Queue()
    outqueue = mp.Manager().Queue()
    for i in range(30):
        inqueue.put(XueweiInfo(i))
    inqueue.put(XueweiInfo('-1'))  # 很重要

    start_time = time.time()

    num_p = 5
    p = []
    for i in range(num_p):
        agent = Agent(inqueue, outqueue)
        # print(agent)
        p.append(mp.Process(target=agent.run, args=()))
        p[i].start()

    for i in range(num_p):
        p[i].join()

    end_time = time.time()
    Logger.debug(end_time - start_time)
