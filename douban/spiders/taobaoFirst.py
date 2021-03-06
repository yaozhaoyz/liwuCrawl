#coding=utf-8
from scrapy.spider import BaseSpider
from scrapy.contrib.spiders import  CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from scrapy.http import FormRequest
from scrapy.http import Request
from scrapy.item import Item
import json
import re
import time 
import datetime

now = datetime.datetime.now()
nowday = now.strftime("%Y%m%d")
seperatorChar = "\t"
taobaoFile=open("/disk2/liwu/taobaoData/"+nowday,'a');

class taobaoSpider(CrawlSpider):	   
#CrawlSpider):
	name = "taobao"
	allowed_domains = ["taobao.com"]

	def start_requests(self):
		search = "http://s.m.taobao.com/search?event_submit_do_new_search_auction=1&_input_charset=utf-8&topSearch=1&atype=b&searchfrom=1&action=home%3Aredirect_app_action&from=1&sst=1&n=20&buying=buyitnow&m=api4h5&abtest=1&wlsort=1&style=list&closeModues=nav%2Cselecthot%2Conesearch&callback=json&q=";
		for term in open("/disk2/liwu/taobao.basicQuery.txt"):
			term = term.strip().strip("\n").strip("\t").replace("\n","")
			count = 0;
			while(count < 44):
				time.sleep(0.1);
				queryStr = search + term + "&page="+ str(count)
				yield Request(queryStr,meta={'query':term},callback=self.parse)
				#yield self.make_requests_from_url(queryStr,meta={'query':term})
				count += 1;

	def parse(self, response):
		query = response.meta['query']
		jsonStr = str(response.body);
		ind = jsonStr.find("json(");
		jsonStr = jsonStr[ind+5:]
		jsonStr = jsonStr.rstrip(");</pre>");
		#taobaoFile.write(jsonStr+"\n")
		jsonMap=  json.loads(jsonStr)
		if( jsonMap["result"] != "true"):
			return "";
		jsonList = jsonMap["listItem"];
		for item in jsonList:
			title =  item["name"].encode('utf8');
			img = item["img2"];
			url = item["url"]
			price = item["price"]
			soldAmount = item["act"]
			taobaoFile.write(query)
			taobaoFile.write(seperatorChar)
			taobaoFile.write(img)
			taobaoFile.write(seperatorChar)
			taobaoFile.write(url)
			taobaoFile.write(seperatorChar)
			taobaoFile.write(title)
			taobaoFile.write(seperatorChar)
			taobaoFile.write("")
			taobaoFile.write(seperatorChar)
			taobaoFile.write("")
			taobaoFile.write(seperatorChar)
			taobaoFile.write(soldAmount)
			taobaoFile.write(seperatorChar)
			taobaoFile.write(price)
			taobaoFile.write("\n")
		return "";
