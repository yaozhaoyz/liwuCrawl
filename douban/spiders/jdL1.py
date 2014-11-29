#coding=utf-8
from scrapy.spider import BaseSpider
from scrapy.contrib.spiders import  CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from scrapy.http import FormRequest
from scrapy.http import Request
from scrapy.item import Item
import re
import datetime

now = datetime.datetime.now()
nowday = now.strftime("%Y%m%d")
seperatorChar = "\t"
jdFile=open("/disk2/liwu/jdData/"+nowday,'a');

class jdSpider(CrawlSpider):	   
#CrawlSpider):
	name = "jd"
	allowed_domains = ["jd.com"]

	def start_requests(self):
		search = "http://search.jd.com/Search?enc=utf8&keyword=";
		for term in open("/disk2/liwu/taobao.basicQuery.txt"):
			term = term.strip().strip("\n").strip("\t")
			count = 0;
			while(count < 44):
				count += 1;
				queryStr = search + term + "&page="+ str(count)
				yield Request(queryStr,meta={'query':term},callback=self.parse)

	def parse(self, response):
		query = response.meta['query']
		query = query.replace("\n","")
		for i in range(1,28):
			hxs = HtmlXPathSelector(response)
			img = hxs.select("//*[@id='plist']/ul/li["+str(i)+"]/div/div[1]/a/img/@data-lazyload")[0].extract();
			itemLink = hxs.select("//*[@id='plist']/ul/li["+str(i)+"]/div/div[2]/a/@href")[0].extract()
			title= hxs.select("//*[@id='plist']/ul/li["+str(i)+"]/div/div[2]/a/text()")[0].extract()
			storeName = "" 
			storeLink = "" 
			soldAmount= hxs.select("//*[@id='plist']/ul/li["+str(i)+"]/div/div[4]/a/text()")[0].extract().replace("已有","").replace("人评价","")
			price= hxs.select("//*[@id='plist']/ul/li["+str(i)+"]/div/div[3]/strong/text()")[0].extract().replace("￥","")
			jdFile.write(query)
			jdFile.write(seperatorChar)
			jdFile.write(img)
			jdFile.write(seperatorChar)
			jdFile.write(itemLink)
			jdFile.write(seperatorChar)
			jdFile.write(title.strip().strip('\t').encode('utf8'))
			jdFile.write(seperatorChar)
			jdFile.write(storeName.encode('utf8'))
			jdFile.write(seperatorChar)
			jdFile.write(storeLink)
			jdFile.write(seperatorChar)
			jdFile.write(soldAmount)
			jdFile.write(seperatorChar)
			jdFile.write(price)
			jdFile.write("\n")
