import scrapy
import re
import json
import logging
import zipfile
import sys


from baiduSoftwares.items import BaidusoftwaresItem
class baiduSpider(scrapy.Spider):
    name = "baiduSpider"
    logger = logging.getLogger()
    def start_requests(self):
        i = 1
        reload(sys)  
        sys.setdefaultencoding('gbk')  
        yield scrapy.Request("http://rj.baidu.com/soft/lists/"+str(16),callback=self.parseList);
      
        yield scrapy.Request("http://rj.baidu.com/soft/lists/"+str(18),callback=self.parseList);
	yield scrapy.Request("http://rj.baidu.com/soft/lists/"+str(17),callback=self.parseList);

        #    i = i + 1

    def parseList(self,response):
        totalP = 0
        matcher = re.findall(r'{.*}',response.xpath("//script")[5].extract())
        
        cont = matcher[0]
        c = json.loads(cont)
        totalP = int(c['data']['page']['totalP'])
       
        i = 1
        while i<=totalP :
            self.logger.info(response.url+"/"+str(i))
            yield scrapy.Request(response.url+"/"+str(i),self.parseSoftwares)
            i = i+ 1
    def parseSoftwares(self, response):
        matcher = re.findall(r'{.*}',response.xpath("//script")[5].extract())
        
        cont = matcher[0]
        c = json.loads(cont)
        soft_list =  c['data']['softList']['list']
        for s in soft_list:
            i = BaidusoftwaresItem()
            i['desc'] =s['soft_desc_short']
            i['name'] = s['soft_name']
            i['soft_update_time'] = s['update_time']
            i['url'] = s['url']
            soft_id = s['soft_id']
            software_page = "http://rj.baidu.com/soft/detail/"+soft_id
            yield  scrapy.Request(software_page,callback=self.parseEach,meta={'item':i},dont_filter=False)
    def parseEach(self, response):
        item = response.meta['item']
        matcher = re.findall(r'{.*}',response.xpath("//script")[5].extract())
        
        
	
	cont = matcher[1]
        c = json.loads(cont)
	version = c['data']['softInfo']['version']
        item['version'] = version        

        yield item
	