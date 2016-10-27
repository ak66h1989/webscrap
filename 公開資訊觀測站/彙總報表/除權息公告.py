
#---- use 除權息計算結果表 instead----

from sqlite3 import *
conn = connect('C:\\Users\\ak66h_000\\Documents\\db\\summary.sqlite3')
c = conn.cursor()

import requests
from bs4 import BeautifulSoup
from numpy import *
from pandas import *
from functools import *
import re

set_option("display.max_columns", 1000)
set_option('display.expand_frame_repr', False)
set_option('display.unicode.east_asian_width', True)

def mymerge(x, y):
    m = merge(x, y, how='outer')
    return m

#---- create table ----
import os
path='C:\\Users\\ak66h_000\\OneDrive\\webscrap\\公開資訊觀測站\\彙總報表\\除權息公告\\'
os.chdir(path)

ys_e = []
year = ['94','95','96','97', '98', '99','100','101','102','103','104']
for y in year:
    try:
        url = 'http://mops.twse.com.tw/mops/web/ajax_t108sb27'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'}
        payload = {'step': '1', 'encodeURIComponent': '1', 'firstin': '1', 'off': '1', 'TYPEK': 'sii', 'year': y}
        source_code = requests.post(url, headers=headers, data=payload)  # should use data instead of params
        source_code.encoding = 'utf8'
        plain_text = source_code.text
        soup = BeautifulSoup(plain_text, 'html.parser')
        h0 = []
        for th in soup.find_all('table')[1].find_all('tr')[0].find_all(rowspan="3"):
            h0.append(th.get_text())
        h1 = []
        for th in soup.find_all('table')[1].find_all('tr')[1].find_all(rowspan="2"):
            h1.append(th.get_text())
        h2 = []
        for th in soup.find_all('table')[1].find_all('tr')[2].find_all('th'):
            h2.append(th.get_text())
        h = h0[0:4] + h2[0:2] + h1[0:1] + h2[2:8] + h1[1:4] + h0[4:]

        tb = [h]
        for tr in soup.find_all('table')[1].find_all('tr')[3:]:
            r = []
            for td in tr.find_all('td'):
                r.append(td.get_text())
            tb.append(r)
        df = DataFrame(tb)
        df.columns = df.ix[0, :]
        df = df.ix[1:len(df), :]
        df.insert(0, '年', int(y) + 1911)
        print(y)
        df.to_csv('{}{}.csv'.format(path, str(int(y) + 1911)), index=False, encoding='utf8')
    except Exception as e:
        print(e)
        ys_e.append([y])
        pass

import os
path = 'C:\\Users\\ak66h_000\\OneDrive\\webscrap\\公開資訊觀測站\\彙總報表\\除權息公告\\'
os.chdir(path)
l = os.listdir()
L=[]
for i in l:
    try:
        df = read_csv(i, encoding='utf8', index_col=False).replace('?', '')
        L.append(df)
    except Exception as e:
        print(e)
        print(i)

df = reduce(mymerge, L)
df=df.dropna(axis=0, subset=['公司名稱']).replace('\xa0', NaN)
df.年=df.年.astype(int)
df.公司代號=df.公司代號.astype(str)
df.股利所屬年度=df.股利所屬年度+1911
df.股利所屬年度=df.股利所屬年度.astype(int).astype(str)
df.drop_duplicates(['年', '公司代號'], inplace=True)

y=df['權利分派基準日'].str.split('/').str[0].astype(int)+1911
y=y.astype(str)
df['權利分派基準日']=y+'/'+df['權利分派基準日'].str.split('/').str[1]+'/'+df['權利分派基準日'].str.split('/').str[2]
y=df['除權交易日'].str.split('/').str[0].astype(float)+1911
y=y.map('{:.0f}'.format).astype(str)
df['除權交易日']=y+'/'+df['除權交易日'].str.split('/').str[1]+'/'+df['除權交易日'].str.split('/').str[2]
y=df['除息交易日'].str.split('/').str[0].astype(float)+1911
y=y.map('{:.0f}'.format).astype(str)
df['除息交易日']=y+'/'+df['除息交易日'].str.split('/').str[1]+'/'+df['除息交易日'].str.split('/').str[2]
y=df['公告日期'].str.split('/').str[0].astype(int)+1911
y=y.astype(str)
df['公告日期']=y+'/'+df['公告日期'].str.split('/').str[1]+'/'+df['公告日期'].str.split('/').str[2]

tablename='除權息公告'
sql = 'create table `{}` (`{}`, PRIMARY KEY ({}))'.format(tablename, '`,`'.join(list(df)), '`年`, `公司代號`')
c.execute(sql)

sql = 'insert into `{}`(`{}`) values({})'.format(tablename, '`,`'.join(list(df)), ','.join('?' * len(list(df))))
c.executemany(sql, df.values.tolist())
conn.commit()

#----update----
# 2016 format is different from previous years unless 2017 comes

#----test----
h0=[]
for th in soup.find_all('table')[1].find_all('tr')[0].find_all(rowspan="3"):
    h0.append(th.get_text())
h1=[]
for th in soup.find_all('table')[1].find_all('tr')[1].find_all(rowspan="2"):
    h1.append(th.get_text())
h2=[]
for th in soup.find_all('table')[1].find_all('tr')[2].find_all('th'):
    h2.append(th.get_text())
h=h0[0:4]+h2[0:2]+h1[0:1]+h2[2:8]+h1[1:4]+h0[4:]

tb=[h]
for tr in soup.find_all('table')[1].find_all('tr')[3:]:
    r=[]
    for td in tr.find_all('td'):
        r.append(td.get_text())
    tb.append(r)
df=DataFrame(tb)
df.columns = df.ix[0, :]
df = df.ix[1:len(df), :]
h0.append(th.get_text())

soup.find_all('table')[1].find_all('tr')[3]

soup.find_all('table')[1].find_all('tr').text()
soup.find_all('table')[1].find_all('tr')[0].find_all(rowspan="2")[0].get_text()