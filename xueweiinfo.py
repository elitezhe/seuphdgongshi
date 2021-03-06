import urllib.request, urllib.error, urllib.parse
from bs4 import BeautifulSoup
import pickle
import os
from logger import Logger


class XueweiInfo(object):
    def __init__(self, xuehao):
        # 检查学号有效性: 长度, 不以230开头
        xuehao = format(xuehao)  # Agent测试时使用,平时没用
        if len(xuehao) == 6:
            pass
        elif xuehao[0:3] == '230':
            xuehao = xuehao[3:]

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
        # self.data_dict = {
        #     'XH': self.xh, 'LX': self.lx, 'YDBRQ': self.ydbrq, 'KTRQ': self.ktrq, 'JSRQ': self.jsrq,
        #     'DD': self.dd, 'XTLY': self.xtly, 'LWZS': self.lwzs, 'TM': self.tm, 'ZTC': self.ztc,
        #     'ZY': self.zy, 'YWTM': self.ywtm, 'YWZTC': self.ywztc, 'YWZY': self.ywzy,
        #     'XSTL': self.xstl, 'XSHY': self.xshy, 'DBZ': self.dbz, 'DBWYH': self.dbwyh, 'DBMS': self.dbms}
        self.data_dict = self.upate_data_dict()

    def get_xh(self):
        return self.xh

    def get_raw(self):
        """
        获取包含答辩信息的HTML页面源码
        :return:
        """
        xw_url = r'http://202.119.4.150/newyjsy/byyxwgl/bssdbxxgsdetail.aspx?xh=%sxw' % self.xh
        request = urllib.request.Request(xw_url)
        response_data = urllib.request.urlopen(request)
        response = response_data.read().decode('gbk').encode('utf-8')
        # response = response.replace("'", '"')  # 替换单引号为双引号
        self.raw = response

    def translate_raw(self):
        """
        将HTML页面中信息提取并保存
        :return:
        """
        # todo 判断raw是否成功获取

        soup = BeautifulSoup(self.raw, "lxml")  # 指定解释器,避免warning
        self.lx = soup.find(id='lbllx').get_text(strip=True)
        # 判断是否有具体数据(空页面)
        if self.lx == '':
            Logger.debug("%s 没有具体信息" % self.get_xh())
            self.lx = 'error'
            raise Exception()

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

        self.data_dict = self.upate_data_dict()

    def upate_data_dict(self):
        self.data_dict = {
            'XH': self.xh, 'LX': self.lx, 'YDBRQ': self.ydbrq, 'KTRQ': self.ktrq, 'JSRQ': self.jsrq,
            'DD': self.dd, 'XTLY': self.xtly, 'LWZS': self.lwzs, 'TM': self.tm, 'ZTC': self.ztc,
            'ZY': self.zy, 'YWTM': self.ywtm, 'YWZTC': self.ywztc, 'YWZY': self.ywzy,
            'XSTL': self.xstl, 'XSHY': self.xshy, 'DBZ': self.dbz, 'DBWYH': self.dbwyh, 'DBMS': self.dbms}
        return self.data_dict

    def save_to_database(self):
        sql = 'UPDATE xuewei SET '
        for key in self.data_dict:
            if key == 'XH':
                continue
            elif key == 'XSTL':
                tmp_str = ''
                for item in self.data_dict['XSTL']:
                    tmp_str = tmp_str + str(item)
                sql = sql + " %s = '%s'," % (key, tmp_str)
            elif key == 'XSHY':
                tmp_str = ''
                for item in self.data_dict['XSHY']:
                    tmp_str = tmp_str + str(item)
                sql = sql + " %s = '%s'," % (key, tmp_str)
            elif key == 'DBZ':
                tmp_str = ''
                for item in self.data_dict['DBZ']:
                    tmp_str = tmp_str + '[' + item + ']'
                sql = sql + " %s = '%s'," % (key, tmp_str)
            elif key == 'DBWYH':
                tmp_str = ''
                for item in self.data_dict['DBWYH']:
                    tmp_str = tmp_str + str(item)
                sql = sql + " %s = '%s'," % (key, tmp_str)
            elif key == 'DBMS':
                tmp_str = ''
                for item in self.data_dict['DBMS']:
                    tmp_str = tmp_str + str(item)
                sql = sql + " %s = '%s'," % (key, tmp_str)
            else:
                sql = sql + " %s = '%s'," % (key, str(self.data_dict[key]))

        sql = sql[0:len(sql)-1]  # 去掉最后一个逗号
        sql = sql + " WHERE XH = '%s'" % self.data_dict['XH']
        return sql

    def read_from_database(self):
        pass

    def pickle_dump(self):
        pickle_path = os.path.join(os.path.curdir, "data")
        pickle_path = os.path.join(pickle_path, "pickle")
        pickle_path = os.path.join(pickle_path, self.xh)
        with open(pickle_path, 'wb') as f:
            pickle.dump(self, f)

    def pickle_load(self):
        """从指定位置的pickle文件中load信息,返回类对象. 注意:不改变本身的信息!!!"""
        pickle_path = os.path.join(os.path.curdir, "data")
        pickle_path = os.path.join(pickle_path, "pickle")
        pickle_path = os.path.join(pickle_path, self.xh)
        with open(pickle_path, 'rb') as f:
            tmp_student = pickle.load(f)
        return tmp_student

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

    def __str__(self):
        return '[%s],[%s],[%s],[%s],[%s];' % (self.zbdw, self.sj, self.dd, self.bgr, self.bgzt)


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

    def __str__(self):
        return '[%s],[%s],[%s],[%s],[%s];' % (self.hymc, self.sj, self.dd, self.brbg, self.bgtm)


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

    def __str__(self):
        return '[%s],[%s],[%s],[%s],[%s],[%s];' % (self.xm, self.zc, self.dslb, self.gzdw, self.sfzx, self.bz)


if __name__ == '__main__':
    xh = '129629'
    # xshy = Xshy(['1','2','3','4','5'])
    student = XueweiInfo(xh)
    student.get_raw()
    student.translate_raw()
    print(student.save_to_database())
    # with open(r'.\data\pickle\129629', 'wb') as f:
    #     pickle.dump(student, f)
    #
    # with open(r'.\data\pickle\129629', 'rb') as f:
    #     student_p = pickle.load(f)

    student.pickle_dump()
    student2 = XueweiInfo(xh)
    student3 = student2.pickle_load()
    print(student2)
    print(student3)

    xh = '149544'
    student1 = XueweiInfo(xh)
    student1.get_raw()
    try:
        student1.translate_raw()
    except:
        Logger.debug('Error')
    print(student1)
