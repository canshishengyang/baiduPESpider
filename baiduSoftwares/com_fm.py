#!/usr/local/bin/python
# -*- coding: utf-8 -*-
import swiftclient
import logging
import os
from com_db_ctrl.com_dbctrl import *
import rados
import MySQLdb

'''
Init Env
'''
LOG_DIR = "/var/log/com_fm"
if not os.path.isdir(LOG_DIR):
    os.mkdir(LOG_DIR)

ERROR_LOG = LOG_DIR + "/com_fm_swift_error.log"

ceph_conf="/etc/ceph/ceph.conf"
if not os.path.isdir("/etc/ceph"):
    error_log("Error: No ceph environment")
    sys.exit(1)


#ceph_conf="/home/guoxiaoyu/varas/gxybeifen/ceph.conf"
#ERROR_LOG="/home/guoxiaoyu/varas/gxybeifen/apitestlog/com_fm_swift_error.log"
HOST="172.18.100.15"
USER="com_fm"
PASSWD="com_fm"
DB="com_fm"


################################################################
'''
swift新接口程序，目前直支持:
    上传文件 def upload(conn,container,filename,filepath)
	conn:swift集群连接实例
	container:上传目标所在容器
	filename:上传至container之后对象名字
	filepath:上传目标文件路径
    下载文件 def download(conn,container,download_filename,save_filepath)	
	conn:swift集群连接实例
	container:下载目标所在容器
	download_filename:下载目标文件名称
	save_filepath:下载目标路径
    删除文件 def delete(conn,container,filename)
 	conn:swift集群连接实例
	container:删除目标文件所在容器
	filename:删除目标文件
    创建容器 def create_container(conn,container)
	conn:swift集群连接实例
	container:目标容器名称
    获取容器列表 def list_container(conn)
	conn:swift集群连接实例
返回值：
    成功返回0
    失败返回-1
    container不存在返回-2
'''
###############################################################
def connect_to_swift():

    conn=swiftclient.Connection(
            user="sf:admin",
            key="sfadmin",
            authurl='http://172.18.202.11:8000/auth/v1.0/'
    )
    return conn

def conn_to_mysql():
    conn=MySQLdb.connect(host=HOST,user=USER,passwd=PASSWD,db=DB)
    cur=conn.cursor()
    return conn,cur
def connect_ceph():
    try:
        cluster=rados.Rados(conffile=ceph_conf)
        cluster.connect()
        return cluster
    except Exception,e:
        error_log(str(e))
        print e
def disconnect_ceph(*argv):
    try:
        cluster=argv[0]
        cluster.shutdown()
    except Exception,e:
        error_log(str(e))
def error_log(content):
    log_name=ERROR_LOG
    try:
        with open(log_name,"a") as f:
            info=str(content)
            f.write(info)
            f.write('\n')
    except Exception,e:
        print e

def swift_st_stat(conn):
    stat_result = {}
    try:
        headers=conn.head_account()
        if not headers.has_key('x-account-object-count') :
            return -3
        if not headers.has_key('x-account-bytes-used') :
            return -3
        object_count = headers['x-account-object-count']
        bytes_used = headers['x-account-bytes-used']
        stat_result['Objects'] = object_count
        stat_result['Bytes'] = bytes_used
    except ClientException as err:
        if SWIFT_NOT_FOUND in str(err):
            return -1
        return -2
    return stat_result
def ceph_st_stat():
    stat_result={}
    try:
        cluster=connect_ceph()
        info=cluster.get_cluster_stats() 
        files_num = info['num_objects'] 
        total=info['kb']
        total="%.2f"%(int(total)/3)
        used=info['kb_used']
        avail=info['kb_avail']
        stat_result['fiels_num']=files_num
        stat_result['total']=total
        stat_result['lb_used']=used
        stat_result['avail']=avail
        disconnect_ceph(cluster)
        print stat_result
    except Exception,e:
        print e
        err_info="ceph_stat err:"+str(e)
        error_log(err_info)
    print stat_result
    return stat_result

def list_container(conn):
    container_list=[]
    for container in conn.get_account()[1]:
	container_list.append(container['name'])
    return container_list
def create_container(container):
    if container not in conn.get_account()[1]:
      	conn.put_container(container)
	return 0
    else:
	return 0
def upload_file(container,filename,filepath,mysql_conn,mysql_cur,conn):
    container_list=list_container(conn)
    if container not in container_list:
            sql='insert into swift_log (result,opeation,filename,container) values ("FAIL","UPLOAD","%s","%s");' %(filename,container)
            mysql_cur.execute(sql)
     	    mysql_conn.commit()
	    error_log("container don't exist")
	    return -2
    else:
    	try:
            f=open(filepath,'r')
            res=conn.put_object(container,filename,contents=f.read(),content_type='text/plain')
  	    sql='insert into swift_log (result,opeation,filename,container) values ("SUCCESS","UPLOAD","%s","%s");' %(filename,container)
            mysql_cur.execute(sql)
            mysql_conn.commit()
	    
	    return os.path.getsize(filepath)
	except Exception,e:
	    log="%s upload fail:%s" %(filename,e)
	    error_log(log)
            sql='insert into swift_log (result,opeation,filename,container) values ("FAIL","UPLOAD","%s","%s");' %(filename,container)
            mysql_cur.execute(sql)
            mysql_conn.commit()
	    return -1
def download_file(container,download_filename,save_filepath,mysql_conn,mysql_cur,conn):
    container_list=list_container(conn)
    if container not in container_list:
            sql='insert into swift_log (result,opeation,filename,container) values ("FAIL","DOWNLOAD","%s","%s");' %(download_filename,container)
            mysql_cur.execute(sql)
            mysql_conn.commit()	
	    error_log("container don't exist")
	    return -2
    else:
	try:
	    obj_tuple=conn.get_object(container,download_filename)
	    file_path=save_filepath+download_filename
            f=open(file_path,'w')
            f.write(obj_tuple[1])
	    length=obj_tuple[0]['content-length']
	    print length
            sql='insert into swift_log (result,opeation,filename,container) values ("SUCCESS","DOWNLOAD","%s","%s");' %(download_filename,container)
            mysql_cur.execute(sql)
            mysql_conn.commit()
	    return length
    	except Exception ,e:
	    log="%s download fail:%s" %(filename,e)
	    error_log(log)
            sql='insert into swift_log (result,opeation,filename,container) values ("FAIL","DOWNLOAD","%s","%s");' %(download_filename,container)
            mysql_cur.execute(sql)
            mysql_conn.commit()
	    return -1
def delete_file(container,filename,mysql_conn,mysql_cur,conn):
    container_list=list_container(conn)
    if container not in container_list:
            sql='insert into swift_log (result,opeation,filename,container) values ("SUCCESS","DELETE","%s","%s");' %(filename,container)
            mysql_cur.execute(sql)
            mysql_conn.commit()
	    error_log("container don't exist")
	    return -2
    else:
        try:
            conn.delete_object(container,filename)
            sql='insert into swift_log (result,opeation,filename,container) values ("SUCCESS","DELETE","%s","%s");' %(filename,container)
            mysql_cur.execute(sql)
            mysql_conn.commit()
	    return 0
        except Exception,e:
	    log="%s delete fail:%s" %(filename,e)
	    error_log(log)
            sql='insert into swift_log (result,opeation,filename,container) values ("FAIL","DELETE","%s","%s");' %(filename,container)
            mysql_cur.execute(sql)
            mysql_conn.commit()
	    return -1
class Swift_Op():
    def __init__(self,storage_type,id=0,flag=1):
	self.flag=flag
	self.storage_type=storage_type
	self.mysql_conn,self.mysql_cur=conn_to_mysql()
        self.conn=connect_to_swift()
    def __del__(self):
	self.mysql_cur.close()
	self.mysql_conn.close()
	self.conn.close()
    def upload(self,*argv):
	    filepath=argv[0]
   	    filename=argv[1]
 	    res=upload_file(self.storage_type,filename,filepath,self.mysql_conn,self.mysql_cur,self.conn)
	    return res
           
    def download(self,*argv):
	    filename=argv[0]
 	    filepath=argv[1]
  	    res=download_file(self.storage_type,filename,filepath,self.mysql_conn,self.mysql_cur,self.conn)
	    return res
    def delete(self,*argv):
            filename=argv[0]
            res=delete_file(self.storage_type,filename,self.mysql_conn,self.mysql_cur,self.conn)
            return res
    def get_stat_info_swift(self,*argv):
	res=swift_st_stat(self.conn)
	return res
    def get_stat_info_ceph(self,*argv):
	res=ceph_st_stat()
	return res
class com_fm(Swift_Op):
    pass 


if __name__ == '__main__':
    op = com_fm("SF_NORMAL")

    print '----Start----'
    for count in range(10):
        res1=op.upload("tests.py","tests.py")
        print "uploads"
        print res1
    
        res2=op.download("tests.py","/tmp/")
        print "download"
        print res2

        res3=op.delete("tests.py","/tmp/")
        print "delete"
        print res3

        res4=op.get_stat_info_swift()
        print "info"
        print res4

        res5=op.get_stat_info_ceph()
        print 'ceph'
        print res5
    print '----Done----'    
