
# -*- coding: UTF-8 -*-
import MySQLdb

from db_operation import connect_to_db
from db_operation import insert_into_db
from db_operation import select_field_from_table
from db_operation import delete_from_table

import time



DB_IP='172.18.100.15'
DB_NAME='savannah_gnu'
DB_USER='savannah'
DB_PASS ='_savannah'


def connect_db():
    
    db =  connect_to_db(DB_IP,DB_USER,DB_PASS,DB_NAME)
   
   
    return db
def data_wash(str_d):
    return str_d
def insert_into_files(scheme,name,s_desc,software_update_time,url,version):
    db = connect_db()
    insert_into_db(db,scheme,
                   "id,name,s_desc,software_update_time,url,version,update_time",
                         "0,'"+data_wash(name)+"','"+data_wash(s_desc)+"','"+data_wash(software_update_time)+"','"+data_wash(url)+"','"+data_wash(version)+"','"+time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())+"'")
                 


            

def select_version_by_pjname(scheme ,name):
        db=connect_db()
        cursor = db.cursor()
        sql = r"select version from "+scheme+r" where name like '"+ data_wash(name)+r"';"
        
        try:
            cursor.execute(sql)
            result = cursor.fetchall()
            print result
            return result
        except Exception,e:
            print e
            return ''




if __name__=='__main__':
	#update_project_record('GNA_projects',1,'wangtua1','desc1','not','date','sdfa','asfd')
    insert_into_files('BaiduFiles', u'\u7231\u5fc3\u50a8\u84c4\u7f50\u5ba2\u6237\u7aef',
                    u'\u65b9\u4fbf\u7528\u6237\u4f7f\u7528\u53d1\u8d77\u7231\u5fc3\u50a8\u84c4\u7f50\u548c\u6d4f\u89c8\u5173\u6ce8\u548c\u70b9\u51fb\u7231\u5fc3\u50a8\u84c4\u7f50',
                        '2013-12-30 13:00:21',
                            u'http://dlsw.baidu.com/sw-search-sp/soft/79/22694/aixinSetup1.7.3636673766.exe',
                                u'1.0.0.7')