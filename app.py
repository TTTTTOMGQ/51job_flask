import MySQLdb
from flask import Flask, render_template, request

import wcprocess

app = Flask(__name__, static_folder='', static_url_path='')
db = MySQLdb.connect("localhost", "root", "123456", "51jobs", charset='utf8')


@app.route('/')
def index():  # put application's code here
    cursor = db.cursor()
    sql ='select count(*) from jobstable'
    cursor.execute(sql)
    count = cursor.fetchall()[0][0]
    # print(data)
    sql = "select round(avg((substring_index(salary,'-',1)+substring_index(substring_index(salary,'-',-1),'万',1))/2*10000),1) from jobstable"
    cursor.execute(sql)
    avg=cursor.fetchall()[0][0]
    # print(avg)
    sql = "select count(*) from (select substring_index(workarea_text,'-',1)  from jobstable group by substring_index(workarea_text,'-',1))s"
    cursor.execute(sql)
    countcity=cursor.fetchall()[0][0]
    # print(countcity)
    sql = "select count(*) from (select company_name from jobstable group by company_name)a"
    cursor.execute(sql)
    countcom=cursor.fetchall()[0][0]
    # print(com)
    return render_template('index.html', count=count,avg=avg,countcity=countcity,countcom=countcom)

@app.route('/index.html')
def home():  # put application's code here
    return index()

@app.route('/tables.html')
def table():
    cursor = db.cursor()######
    sql = "select job_name,company_name,salary,workarea_text,experience,education,job_href,company_href from jobstable"
    datalist = []
    cursor.execute(sql)
    joblist = cursor.fetchall()
    # print(joblist)
    for i in joblist:
        datalist.append(i)
    cursor.close()
    return render_template('tables.html', datalist=datalist)

@app.route('/map.html', methods=['POST', 'GET'])
def map():
    cursor = db.cursor()
    sql1 = "select substring_index(workarea_text,'-',1) as name,count(substring_index(workarea_text,'-',1))as value from jobstable "
    sql2 = "group by substring_index(workarea_text,'-',1)"
    datalist = []
    if request.method == 'POST' and request.form.get('keyword') != '':
        sql1 = sql1 + "where concat(company_name,job_name,education,salary,companyind_text," \
                      "companysize_text,companytype_text,jobwelf,job_msg) like '%" + request.form.get('keyword') + "%'"
    sql = sql1 + sql2
    cursor.execute(sql)
    citylist = cursor.fetchall()
    # print(citylist)
    for i in citylist:
        dit = {'name': i[0], 'value': i[1]}
        datalist.append(dit)
    cursor.close()
    return render_template('charts_city.html', data=datalist)

@app.route('/pie.html', methods=['POST', 'GET'])
def pie():
    cursor = db.cursor()
    p_sql = "select experience ,count(experience) from jobstable group by experience"
    d_sql = "select education ,count(education) from jobstable group by education"
    ep_list = []
    ed_list = []
    if request.method == 'POST':
        if type(request.form.get('dkeyword')).__name__ != 'NoneType':
            # print(type(request.form.get('pkeyword')))
            sqllist = list(d_sql)
            sqllist.insert(49,
                           " where concat(company_name,job_name,education,salary,companyind_text,companysize_text,companytype_text,jobwelf,job_msg) like '%" + request.form.get(
                               'dkeyword') + "%'")
            sql = ''.join(sqllist)
            # print(sql)
            cursor.execute(sql)
            ed_data = cursor.fetchall()
            for i in ed_data:
                dit = {
                    "name": i[0],
                    "value": i[1]
                }
                if dit['name']=='':
                    dit['name'] = '无学历要求'
                ed_list.append(dit)
        else:
            cursor.execute(d_sql)
            ed_data = cursor.fetchall()
            for i in ed_data:
                dit = {
                    "name": i[0],
                    "value": i[1]
                }
                if dit['name'] == '':
                    dit['name'] = '无学历要求'
                ed_list.append(dit)
        if type(request.form.get('pkeyword')).__name__ != 'NoneType':
            sqllist = list(p_sql)
            sqllist.insert(51,
                           " where concat(company_name,job_name,education,salary,companyind_text,companysize_text,companytype_text,jobwelf,job_msg) like '%" + request.form.get(
                               'pkeyword') + "%'")
            sql = ''.join(sqllist)
            print(sql)
            cursor.execute(sql)
            ep_data = cursor.fetchall()
            for i in ep_data:
                dit = {
                    "name": i[0],
                    "value": i[1]
                }
                ep_list.append(dit)
        else:
            cursor.execute(p_sql)
            ep_data = cursor.fetchall()
            for i in ep_data:
                dit = {
                    "name": i[0],
                    "value": i[1]
                }
                ep_list.append(dit)
    else:
        cursor.execute(p_sql)
        ep_data = cursor.fetchall()
        for i in ep_data:
            dit = {
                "name": i[0],
                "value": i[1]
            }
            ep_list.append(dit)
        cursor.execute(d_sql)
        ed_data = cursor.fetchall()
        for i in ed_data:
            dit = {
                "name": i[0],
                "value": i[1]
            }
            ed_list.append(dit)
    cursor.close()
    return render_template("charts_pie.html", pdata=ep_list, ddata=ed_list)

@app.route('/csalary.html', methods=['POST', 'GET'])
def csalary():
    cursor = db.cursor()
    sql = '''
    select substring_index(workarea_text,'-',1),
    round(avg((substring_index(salary,'-',1)+substring_index(substring_index(salary,'-',-1),'万',1))/2*10000),0) 
    from jobstable 
    group by substring_index(workarea_text,'-',1) 
    order by avg((substring_index(salary,'-',1)+substring_index(substring_index(salary,'-',-1),'万',1))/2*10000)desc
    '''
    if request.method == 'POST' and type(request.form.get('keyword')).__name__ != 'NoneType':
        sql = list(sql)

        sql.insert(181, " where concat(job_name,education,experience) like '%" + request.form.get(
            'keyword') + "%'")
        sql = ''.join(sql)
        # print(sql)
    cursor.execute(sql)
    city = []
    salary = []
    datalist = cursor.fetchall()
    for item in datalist:
        city.append(item[0])
        salary.append(item[1])
    return render_template('charts_salary.html', city=city, salary=salary)

@app.route('/esalary.html', methods=['POST', 'GET'])
def esalary():
    cursor = db.cursor()
    psql = '''
    select experience,
    round(avg((substring_index(salary,'-',1)+substring_index(substring_index(salary,'-',-1),'万',1))/2*10000),0) as s 
    from jobstable group by experience order by s
    '''
    dsql = '''
    select education,avg((substring_index(salary,'-',1)+substring_index(substring_index(salary,'-',-1),'万',1))/2*10000) as s 
    from jobstable group by education order by s desc
    '''
    if request.method == 'POST':
        if type(request.form.get('dkeyword')).__name__ != 'NoneType':
            dsql = list(dsql)
            dsql.insert(145, " where job_name like '%"+request.form.get(
                'dkeyword')+"%'")
            dsql = ''.join(dsql)
            print(dsql)
        if type(request.form.get('pkeyword')).__name__ != 'NoneType':
            psql = list(psql)
            psql.insert(160, " where job_name like '%"+request.form.get(
                'pkeyword')+"%'")
            psql = ''.join(psql)
            print(psql)
    exp = []
    edu = []
    psalary = []
    dsalary = []
    cursor.execute(psql)
    datalist = cursor.fetchall()
    for item in datalist:
        exp.append(item[0])
        psalary.append(item[1])
    cursor.execute(dsql)
    datalist = cursor.fetchall()
    for item in datalist:
        if item[0] == '':
            edu.append('无要求')
            dsalary.append(item[1])
            continue
        edu.append(item[0])
        dsalary.append(item[1])
    cursor.close()
    return render_template('charts_esalary.html', exp=exp,edu=edu, dsalary=dsalary, psalary=psalary)

@app.route('/wordcloud.html', methods=['POST', 'GET'])
def wcpic():
    wsql = '''
    select jobwelf from jobstable
    '''
    msql='''
    select job_msg from jobstable
    '''
    cursor = db.cursor()
    if request.method == 'POST':
        if type(request.form.get('wkeyword')).__name__ != 'NoneType':
            wsql = wsql + " where job_name like '%"+request.form.get('wkeyword')+"%'"
        if type(request.form.get('mkeyword')).__name__ != 'NoneType':
            msql = msql + " where job_name like '%"+request.form.get('mkeyword')+"%'"
        cursor.execute(wsql)
        data = cursor.fetchall()
        wcprocess.welf(data)
        cursor.execute(msql)
        data = cursor.fetchall()
        wcprocess.msg(data)
        cursor.close()
    return render_template('charts_wordcloud.html')

if __name__ == '__main__':
    app.run()
