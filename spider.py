# -*- codeing = utf-8 -*-
# !/home/ubuntu/.virtualenvs/env38 python
import json
import re
import time
import execjs
import zlib
import urllib.request, urllib.error
from urllib import parse
from bs4 import BeautifulSoup
from app import db

js = '''
var _0x5e8b26 = '3000176000856006061501533003690027800375'

var getAcwScV2 = function (arg1) {
    String['prototype']['hexXor'] = function (_0x4e08d8) {
        var _0x5a5d3b = '';
        for (var _0xe89588 = 0x0; _0xe89588 < this['length'] && _0xe89588 < _0x4e08d8['length']; _0xe89588 += 0x2) {
            var _0x401af1 = parseInt(this['slice'](_0xe89588, _0xe89588 + 0x2), 0x10);
            var _0x105f59 = parseInt(_0x4e08d8['slice'](_0xe89588, _0xe89588 + 0x2), 0x10);
            var _0x189e2c = (_0x401af1 ^ _0x105f59)['toString'](0x10);
            if (_0x189e2c['length'] == 0x1) {
                _0x189e2c = '0' + _0x189e2c;
            }
            _0x5a5d3b += _0x189e2c;
        }
        return _0x5a5d3b;
    };
    String['prototype']['unsbox'] = function () {
        var _0x4b082b = [0xf, 0x23, 0x1d, 0x18, 0x21, 0x10, 0x1, 0x26, 0xa, 0x9, 0x13, 0x1f, 0x28, 0x1b, 0x16, 0x17, 0x19, 0xd, 0x6, 0xb, 0x27, 0x12, 0x14, 0x8, 0xe, 0x15, 0x20, 0x1a, 0x2, 0x1e, 0x7, 0x4, 0x11, 0x5, 0x3, 0x1c, 0x22, 0x25, 0xc, 0x24];
        var _0x4da0dc = [];
        var _0x12605e = '';
        for (var _0x20a7bf = 0x0; _0x20a7bf < this['length']; _0x20a7bf++) {
            var _0x385ee3 = this[_0x20a7bf];
            for (var _0x217721 = 0x0; _0x217721 < _0x4b082b['length']; _0x217721++) {
                if (_0x4b082b[_0x217721] == _0x20a7bf + 0x1) {
                    _0x4da0dc[_0x217721] = _0x385ee3;
                }
            }
        }
        _0x12605e = _0x4da0dc['join']('');
        return _0x12605e;
    };
    var _0x23a392 = arg1['unsbox']();
    arg2 = _0x23a392['hexXor'](_0x5e8b26);
    return arg2
};
'''
# 爬取的链接
''' 
    https://search.51job.com/list/000000,000000,0000,01,0,99,%25E5%25BC%2580%25E5%258F%2591,2,1.html 开发 24h
    https://search.51job.com/list/000000,000000,0000,01,0,99,%25E6%25B5%258B%25E8%25AF%2595,2,1.html 测试 24h
    https://search.51job.com/list/000000,000000,0000,01,0,99,%25E8%25BF%2590%25E7%25BB%25B4,2,1.html 运维 24h
'''


def main():
    with open('keyword.txt', 'r', encoding='UTF-8') as f:
        klist = json.load(f)
    # html = askURL('https://search.51job.com/list/000000,000000,0000,01,3,99,%25E5%25BC%2580%25E5%258F%2591,2,1.html')
    # 开发关键词
    # html = askURL('https://jobs.51job.com/shanghai/139778546.html')
    search_link = 'https://search.51job.com/list/000000,000000,0000,01,0,99,'
    init_database()
    
    for item in klist['keyword']:
        i = 1
        while (i < klist['page'] + 1):
            url = search_link + parse.quote(parse.quote(item)) + ',2,' + str(i) + '.html'
            print(url)
            joblist = []
            select_data(askURL(url), joblist)
            save_data(joblist)
            i += 1


def askURL(url):
    # 模拟浏览器头部信息,向服务器发送消息
    head = {
        "acw_sc__v2": "2f624a4316541475054072307e705699de6bf1cd2ac9a9fd31d038f3084db9",
        "cookie": "",
        "User-Agent": ""}  # 用户代理
    request = urllib.request.Request(url, headers=head)
    html = ""
    try:
        response = urllib.request.urlopen(request)
        if response.getheader('Content-Encoding') == 'gzip':
            # 如果是详情页则先解压缩解密再二次请求
            content = zlib.decompress(response.read(), 32 + zlib.MAX_WBITS).decode()
            arg1 = re.findall("arg1='(\S+)'", str(content))[0]
            node = execjs.get()
            ctx = node.compile(js)
            arg2 = ctx.call("getAcwScV2", arg1)
            head["cookie"] = 'acw_sc__v2=' + arg2
            head['acw_tc'] = '76b20fef16524218174844287e26d5'
            request = urllib.request.Request(url, headers=head)
            response = urllib.request.urlopen(request)
            html = response.read().decode('gbk')
        else:
            html = response.read().decode('gbk')
    except urllib.error.URLError as e:
        if hasattr(e, "code"):
            print(e.code)
        if hasattr(e, "reason"):
            print(e.reason)
        html = ''
    except IOError as io:
        print(io)
    return html


def select_data(html, joblist):
    # html = open("./testHtml/joblist.html", "rb").read().decode('gbk')
    html_data = re.findall('window.__SEARCH_RESULT__ = (.*?)</script>', html)[0]
    json_data = json.loads(html_data)
    for index in json_data['engine_jds']:
        print(index['job_href'])
        job_msg = str(select_page_data(index['job_href']))
        if len(index['attribute_text']) == 2:
            if index['attribute_text'][1].find('经验') != -1:
                education = ''
                experience = index['attribute_text'][1]
            else:
                education = index['attribute_text'][1]
                experience = ''
        elif len(index['attribute_text']) == 1:
            education = ''
            experience = ''
        else:
            education = index['attribute_text'][2]
            experience = index['attribute_text'][1]
        dit = {
            'jobid': index['jobid'],
            '标题': index['job_name'],
            '公司名字': index['company_name'],
            '城市': index['workarea_text'],
            '经验要求': experience,
            '学历要求': education,
            '薪资': index['providesalary_text'],
            '公司属性': index['companyind_text'],
            '公司规模': index['companysize_text'],
            '企业性质': index['companytype_text'],
            '招聘发布日期': index['issuedate'],
            '公司详情页': index['company_href'],
            '招聘详情页': index['job_href'],
            '工作福利': '|'.join(index['jobwelf_list']),
            '详细信息': job_msg
        }
        joblist.append(dit)


def select_page_data(job_href):
    # html = askURL('https://jobs.51job.com/shanghai/139778546.html')
    try:
        html = askURL(job_href)
    except:
        job_msg = '岗位已丢失'
        return job_msg
    bs = BeautifulSoup(html, 'html.parser')
    job_msg = bs.select('.tBorderTop_box > .bmsg')[0].text.strip().replace('\r', '').replace('\n', '').replace('\xa0',
                                                                                                               '')
    time.sleep(15)
    return job_msg


def init_database():
    sql = '''
    create table IF NOT EXISTS jobstable (
    jobid int primary key,
    job_name text,
    company_name text,
    workarea_text text,
    experience text,
    education text,
    salary text,
    companyind_text text,
    companysize_text text,
    companytype_text text,
    issuedate text,
    company_href text,
    job_href text,
    jobwelf text,
    job_msg text
    )
    '''
    cursor = db.cursor()
    cursor.execute(sql)
    print('数据库初始化完成')


def save_data(joblist):
    cursor = db.cursor()
    cursor.executemany("""
    INSERT IGNORE INTO
    jobstable (jobid,
    job_name,
    company_name,
    workarea_text,
    experience,
    education,
    salary,
    companyind_text,
    companysize_text,
    companytype_text,
    issuedate,
    company_href,
    job_href,
    jobwelf,
    job_msg)
    VALUES
    (%(jobid)s,
    %(标题)s, %(公司名字)s,
    %(城市)s, %(经验要求)s,
    %(学历要求)s,
    %(薪资)s,
    %(公司属性)s,
    %(公司规模)s,
    %(企业性质)s,
    %(招聘发布日期)s,
    %(公司详情页)s,
    %(招聘详情页)s,
    %(工作福利)s,
    %(详细信息)s)""", joblist)
    db.commit()


def format_data():
    cursor = db.cursor()
    sql = "select jobid,salary from jobstable where salary like '%千%';"
    cursor.execute(sql)
    result = cursor.fetchall()
    try:
        for i in result:
            salary = '0.' + i[1][:1] + '-0.' + i[1][2:3] + '万/月'
            update = "update jobstable set salary='%s' where jobid='%s'" % (salary, i[0])
            cursor.execute(update)
            db.commit()
    except Exception as e:
        print(e)
        db.rollback()
    sql = "select jobid,salary from jobstable where salary like '%年%';"
    cursor.execute(sql)
    result = cursor.fetchall()
    try:
        for i in result:
            print(i[1][0:-3].split('-'))
            s = i[1][0:-3].split('-')
            salary = str(round(int(s[0]) / 12, 1)) + '-' + str(round(int(s[1]) / 12, 1)) + '万/月'
            update = "update jobstable set salary='%s' where jobid='%s'" % (salary, i[0])
            cursor.execute(update)
            db.commit()
    except Exception as e:
        print(e)
    cursor.close()


if __name__ == '__main__':
    start = time.time()
    main()
    end = time.time()
    db.close()
    print(end - start)
