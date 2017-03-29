# -*- coding: utf-8 -*-

import urllib2
from bs4 import BeautifulSoup


class XueweiInfo(object):
    def __init__(self, xuehao):
        self.xh = xuehao  # 学号
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
        获取包含答辩信息的HTML页面源码
        :return:
        """
        xw_url = ur'http://202.119.4.150/newyjsy/byyxwgl/bssdbxxgsdetail.aspx?xh=%sxw' % self.xh
        request = urllib2.Request(xw_url)
        response_data = urllib2.urlopen(request)
        response = response_data.read().decode('gb2312').encode('utf-8')
        self.raw = response

    def translate_raw(self):
        """
        将HTML页面中信息提取并保存
        :return:
        """
        # todo 判断raw是否成功获取

        soup = BeautifulSoup(self.raw)
        self.lx = soup.find(id='lbllx').get_text(strip=True)
        self.ydbrq = soup.find(id='lbldbrq').get_text(strip=True)
        # todo 补全其他

    def save_to_database(self):
        pass

    def read_from_database(self):
        pass


class Xstl(object):
    """学术讨论"""
    def __init__(self):
        # 主办单位 时间 地点 报告人 报告主题
        self.zbdw = u''
        self.sj = u''
        self.dd = u''
        self.bgr = u''
        self.bgzt = u''

    def set_from_list(self, infolist):
        pass

    def get_printable(self):
        pass


class Xshy(object):
    """学术会议"""
    def __init__(self):
        # 会议名称 时间 地点 本人报告 本人报告题目
        self.hymc = u''
        self.sj = u''
        self.dd = u''
        self.brbg = u''
        self.bgtm = u''

    def set_from_list(self, infolist):
        self.hymc = ''


class Dbwy(object):
    """答辩委员会和答辩秘书信息"""
    def __init__(self):
        # 姓名 职称 导师类别 工作单位 是否主席 备注
        self.xm = u''
        self.zc = u''
        self.dslb = u''
        self.gzdw = u''
        self.sfzx = u''
        self.bz = u''

    def set_from_list(self, infolist):
        pass


if __name__ == '__main__':
    pass
