# -*- coding: utf-8 -*-

import urllib.request, urllib.error, urllib.parse
from bs4 import BeautifulSoup


class XueweiInfo(object):
    def __init__(self, xuehao):
        self.xh = xuehao  # 学号
        self.raw = ''  # HTML page
        self.lx = ''  # 类型
        self.ydbrq = ''  # 预答辩日期
        self.ktrq = ''  # 开题日期
        self.jsrq = ''  # 结束日期
        self.dd = ''  # 地点
        self.xtly = ''  # 选题来源
        self.lwzs = 0.0  # 论文字数(万字)
        self.tm = ''  # 题目
        self.ztc = ''  # 主题词
        self.zy = ''  # 摘要
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
        xw_url = r'http://202.119.4.150/newyjsy/byyxwgl/bssdbxxgsdetail.aspx?xh=%sxw' % self.xh
        request = urllib.request.Request(xw_url)
        response_data = urllib.request.urlopen(request)
        response = response_data.read().decode('gbk').encode('utf-8')
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
        self.ktrq = soup.find(id='lblksrq').get_text(strip=True)
        self.jsrq = soup.find(id='lbljsrq').get_text(strip=True)  # 结束日期
        self.dd = soup.find(id='lbldbdd').get_text(strip=True)  # 地点
        self.xtly = soup.find(id='lbllwxtly').get_text(strip=True)  # 选题来源
        self.lwzs = float(soup.find(id='lbllwzs').get_text(strip=True))  # 论文字数(万字)
        self.tm = soup.find(id='lbllwtm').get_text(strip=True)  # 题目
        self.ztc = soup.find(id='lbllwztc').get_text(strip=True)  # 主题词
        self.zy = soup.find(id='lbllwzy').get_text(strip=True)  # 摘要
        self.ywtm = soup.find(id='lbllwywtm').get_text(strip=True)  # 英文题目
        self.ywztc = soup.find(id='lbllwywztc').get_text(strip=True)  # 英文主题词
        self.ywzy = soup.find(id='lbllwywzy').get_text(strip=True)  # 英文摘要

        table_xstl_soup = soup.find(id="dgDataXstl")
        xstl = []
        for tr in table_xstl_soup.find_all('tr'):
            td = tr.find_all('td')
            td_l = []
            for tdd in td:
                tmp_txt = tdd.get_text(strip=True)
                if len(tmp_txt) > 0:
                    td_l.append(tmp_txt)
                else:
                    break
            if len(td_l) > 0:
                xstl.append(td_l)
            else:
                break
        xstl = xstl[1:]
        for item in xstl:
            self.xstl.append(Xstl(item))

        table_xshy_soup = soup.find(id="dgDataXshy")
        xshy = []
        for tr in table_xshy_soup.find_all('tr'):
            td = tr.find_all('td')
            td_l = []
            for tdd in td:
                tmp_txt = tdd.get_text(strip=True)
                if len(tmp_txt) > 0:
                    td_l.append(tmp_txt)
                else:
                    break
            if len(td_l) > 0:
                xshy.append(td_l)
            else:
                break
        xshy = xshy[1:]
        for item in xshy:
            self.xshy.append(Xshy(item))

        table_dbz_soup = soup.find(id="dgDatadbz")
        dbz = []
        for tr in table_dbz_soup.find_all('tr'):
            td = tr.find('td')
            tmp_txt = td.get_text(strip=True)
            if len(tmp_txt) > 0:
                dbz.append(tmp_txt)
        self.dbz = dbz

        table_dbwyh_soup = soup.find(id="dgData")
        dbwyh = []
        for tr in table_dbwyh_soup.find_all('tr'):
            td = tr.find_all('td')
            td_l = []
            td_first_col = True
            for tdd in td:
                tmp_txt = tdd.get_text(strip=True)
                if len(tmp_txt) == 0 and td_first_col:
                    break
                td_l.append(tmp_txt)
                td_first_col = False
            if len(td_l) > 0:
                dbwyh.append(td_l)
            else:
                break
        dbwyh = dbwyh[1:]
        for item in dbwyh:
            self.dbwyh.append(Dbwy(item))

        table_dbms_soup = soup.find(id="dgDatams")
        dbms = []
        for tr in table_dbms_soup.find_all('tr'):
            td = tr.find_all('td')
            td_l = []
            td_first_col = True
            for tdd in td:
                tmp_txt = tdd.get_text(strip=True)
                if len(tmp_txt) == 0 and td_first_col:
                    break
                td_l.append(tmp_txt)
                td_first_col = False
            if len(td_l) > 0:
                dbms.append(td_l)
            else:
                break
        dbms = dbms[1:]
        for item in dbms:
            self.dbms.append(Dbwy(item))


    def save_to_database(self):
        pass

    def read_from_database(self):
        pass


class Xstl(object):
    """学术讨论"""
    def __init__(self, infolist):
        # 主办单位 时间 地点 报告人 报告主题
        if len(infolist) == 5:
            self.zbdw = infolist[0]
            self.sj = infolist[1]
            self.dd = infolist[2]
            self.bgr = infolist[3]
            self.bgzt = infolist[4]
        else:
            self.zbdw = ''
            self.sj = ''
            self.dd = ''
            self.bgr = ''
            self.bgzt = ''

    def set_from_list(self, infolist):
        if len(infolist) == 5:
            self.zbdw = infolist[0]
            self.sj = infolist[1]
            self.dd = infolist[2]
            self.bgr = infolist[3]
            self.bgzt = infolist[4]

    def get_printable(self):
        pass


class Xshy(object):
    """学术会议"""
    def __init__(self, infolist=[]):
        # 会议名称 时间 地点 本人报告 本人报告题目
        if len(infolist) == 5:
            self.hymc = infolist[0]
            self.sj = infolist[1]
            self.dd = infolist[2]
            self.brbg = infolist[3]
            self.bgtm = infolist[4]
        else:
            self.hymc = ''
            self.sj = ''
            self.dd = ''
            self.brbg = ''
            self.bgtm = ''

    def set_from_list(self, infolist):
        if len(infolist) == 5:
            self.hymc = infolist[0]
            self.sj = infolist[1]
            self.dd = infolist[2]
            self.brbg = infolist[3]
            self.bgtm = infolist[4]


class Dbwy(object):
    """答辩委员会和答辩秘书信息"""
    def __init__(self, infolist=[]):
        # 姓名 职称 导师类别 工作单位 是否主席 备注
        if len(infolist) == 6:
            self.xm = infolist[0]
            self.zc = infolist[1]
            self.dslb = infolist[2]
            self.gzdw = infolist[3]
            self.sfzx = infolist[4]
            self.bz = infolist[5]
        elif len(infolist) == 4:
            self.xm = infolist[0]
            self.zc = infolist[1]
            self.dslb = ''
            self.gzdw = infolist[2]
            self.sfzx = ''
            self.bz = infolist[3]
        else:
            self.xm = ''
            self.zc = ''
            self.dslb = ''
            self.gzdw = ''
            self.sfzx = ''
            self.bz = ''

    def set_from_list(self, infolist):
        if len(infolist) == 6:
            self.xm = infolist[0]
            self.zc = infolist[1]
            self.dslb = infolist[2]
            self.gzdw = infolist[3]
            self.sfzx = infolist[4]
            self.bz = infolist[5]
        elif len(infolist) == 4:
            self.xm = infolist[0]
            self.zc = infolist[1]
            self.dslb = ''
            self.gzdw = infolist[2]
            self.sfzx = ''
            self.bz = infolist[3]


if __name__ == '__main__':
    xh = '129629'
    # xshy = Xshy(['1','2','3','4','5'])
    student = XueweiInfo(xh)
    student.get_raw()
    student.translate_raw()
    print(student)


