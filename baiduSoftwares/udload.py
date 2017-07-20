#!/usr/bin/python
# -*- coding: UTF-8 -*-


from poster.encode import multipart_encode
from poster.streaminghttp import register_openers
import urllib2
import random
import time
import com_fm

RackeeperHOST="172.18.108.122"
RackeeperPORT="80"
ContainerVip = "RA_VIP"
ContainerNormal = "RA_NORMAL"
ImasDevUser = "ra:admin"
ImasDevPass = "raadmin"


"""
    Upload a local file to CommonStorage
    Parameters:
        path, a file in current folder, type of string
    Return:
        status, True if success otherwise False
"""
def upload_to_commonstorage(path):
    try:
        op = com_fm.com_fm("SF_NORMAL")

        random.seed()

        count = 3
        while count > 0:
            
            result = op.upload(path, str(path).split('/')[-1])   
            if result >= 0:
		print 'success'
                return True

            count = count - 1
            time.sleep(random.randint(1, 10))

        return False

    except Exception,e:
        print e
        return False


'''
"""
    Upload a local file to CommonStorage
    Parameters:
        path, a file in current folder, type of string
    Return:
        status, True if success otherwise False
"""
def upload_to_commonstorage(path):
    try:
        url = "http://" +RackeeperHOST+ "/com-sm/upload-file/"

        random.seed()

        count = 3
        while count > 0:
            register_openers()
            datagen, headers = multipart_encode({"upload_file": open(path,"rb"),"storage_type":"ra","filename":path,"username":ImasDevUser,"password":ImasDevPass})
            request = urllib2.Request(url, datagen, headers)
            result = urllib2.urlopen(request).read()

            print result

            if r'success' in result:
                return True

            count = count - 1
            time.sleep(random.randint(1, 10))
        
        return False

    except Exception,e:
        print e
        return False 
'''

"""
    Download a file from CommonStorage to local drive
    Parameters:
        uri, filename in CommonStorage, type of string
        path, path in local drive, type of string
    Return:
        status, True if success otherwise False
"""
def download_from_commonstorage(uri,path):
    try:

        op = com_fm.com_fm("SF_NORMAL")
        
        soft_content = op.download(uri, path)

        # download failed
        if soft_content < 0:
            return False

        return True

    except Exception,e:
        print e
        return False


'''
"""
    Download a file from CommonStorage to local drive
    Parameters:
        uri, filename in CommonStorage, type of string
        path, path in local drive, type of string
    Return:
        status, True if success otherwise False
"""
def download_from_commonstorage(uri,path):
    try:

        url = "http://" + RackeeperHOST + "/com-sm/download-file/"

        register_openers()
        datagen, headers = multipart_encode({"storage_type":"ra","filename":uri,"username":ImasDevUser,"password":ImasDevPass})
        request = urllib2.Request(url, datagen, headers)
        soft_content = urllib2.urlopen(request).read()

        # download failed
        if(r'<xml>' in soft_content):
            print 'download file failed',soft_content
            return False

        f = open(path,"wb")
        f.write(soft_content)
        f.close()

        return True

    except Exception,e:
        print e
        return False
'''


"""
    Delete a file in CommonStorage
    Parameters:
        uri, filename in CommonStorage, type of string
    Return:
        status, True if success otherwise False
"""
def del_from_commonstorage(uri):
    try:

        op = com_fm.com_fm("SF_NORMAL")

        result = op.delete(uri)

        if result >= 0:
            return True

        # print result
        return False

    except Exception as e:
        print e
        return False


"""
    Delete a file in CommonStorage
    Parameters:
        uri, filename in CommonStorage, type of string
    Return:
        status, True if success otherwise False
"""
def del_from_commonstorage(uri):
    try:

        url = "http://" +RackeeperHOST+ "/com-sm/delete-file/"

        register_openers()
        datagen, headers = multipart_encode({"storage_type":"ra","filename":uri,"username":ImasDevUser,"password":ImasDevPass})
        request = urllib2.Request(url, datagen, headers)
        result = urllib2.urlopen(request).read()

        if r'success' in result:
            return True

        # print result
        return False
    
    except Exception as e:
        print e
        return False
if __name__=="__main__":
#		upload_to_commonstorage('wsy.txt')
		download_from_commonstorage('f97fc6a634d325cb1dd5d5f49a99669e9fa42d4d.zip','download.txt')	
#uri=upload_to_cloud('test1.txt')
#print uri

#download_from_cloud('a6e2db353c2eca0bbbed174ea0fd9d73','.txt')

#del_from_cloud('b9e6ac8a7811c0f8ff9cab07e7c59b42')

#print random.randint(0,5)
#result=download_from_cloud_2('683a123b916d49173b8e8528d16abbb5',"c:\\varas\\result\\dynamic.dot")
#print result
    
