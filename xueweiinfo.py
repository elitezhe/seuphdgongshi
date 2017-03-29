# -*- coding: utf-8 -*-

import urllib2


class XueweiInfo(object):
    def __init__(self):
        self.xh = ''  # 学号
        self.raw = u''  # HTML page
        self.lx = u''  # 类型
        self.ydbrq = u''  # 预答辩日期
        self.ktrq = u''  # 开题日期
        self.jsrq = u''  # 结束日期
        self.dd = u''  # 地点
        self.xtly = u''  # 选题来源
        self.lwzs = 0.0  # 论文字数(万字)
        self.tm = u''  # 题目
        self.ztc = u''  # 主题词
        self.zy = u''  # 摘要
        self.ywtm = ''  # 英文题目
        self.ywztc = ''  # 英文主题词
        self.ywzy = ''  # 英文摘要
        self.xstl = []  # 学术讨论 [主办单位 时间 地点 报告人 报告主题]
        self.xshy = []  # 学术会议 [会议名称 时间 地点 本人报告 本人报告题目]
        self.dbz = []  # 代表作 [论文名称]
        self.dbwyh = []  # 答辩委员会组成 [姓名 职称 导师类别 工作单位 是否主席 备注]
        self.dbms = []  # 答辩秘书 [姓名 职称 工作单位 备注]

    def get_raw(self):
        """

        :return:
        """
        xw_url = ur'http://202.119.4.150/newyjsy/byyxwgl/bssdbxxgsdetail.aspx?xh=%sxw' % self.xh


