# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.pipelines.files import FilesPipeline
import MySQLdb
import scrapy
import os
import zipfile
import logging
from baiduSoftwares.udload import upload_to_commonstorage

from baiduSoftwares.DAO import select_version_by_pjname
from baiduSoftwares.DAO import insert_into_files

class BaidusoftwaresPipeline(object):
    def process_item(self, item, spider):
        
        return item
class DownloadPipelines(FilesPipeline):
    logger = logging.getLogger()
    def get_media_requests(self, item, info):
        version = select_version_by_pjname('BaiduFiles',item['name'])
        if not version:
            
                yield scrapy.Request(item['url'])                 
          
        else:
            need_upload = True
            for v in version[0]:
                if v == item['version']:
                   need_upload = False
            if need_upload == True:
                
                       yield scrapy.Request(item['url'])                 
               

    def item_completed(self, results, item, info):
        for tp in results:
            if tp[0]==True:
                     filename ='./codes/full/'+str(tp[1]['path']).split('/')[-1].replace("exe","zip") 
                     
                     try:
                                           
                        zip = zipfile.ZipFile(filename,"w");
                        zip.write('./codes/full/'+str(tp[1]['path']).split('/')[-1],str(tp[1]['path']).split('/')[-1])
                        zip.close()
                        self.logger.info("file name "+filename)
                        upload_to_commonstorage(filename)
                        insert_into_files('BaiduFiles',
				item['name'],
					item['desc'],
						item['soft_update_time'],
							filename.split('/')[-1],
								item['version'])
                     finally:
                      
                        if os.path.exists(filename):
                            os.remove(filename)
                        if os.path.exists('./codes/full/'+str(tp[1]['path']).split('/')[-1]):
                            os.remove('./codes/full/'+str(tp[1]['path']).split('/')[-1])
                              