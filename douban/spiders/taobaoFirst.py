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
taobaoFile=open("/disk2/liwu/taobaoData/"+nowday,'a');

class taobaoSpider(CrawlSpider):	   
#CrawlSpider):
	name = "taobao"
	allowed_domains = ["taobao.com"]

	def start_requests(self):
		search = "http://s.taobao.com/search?q=";
		for term in open("/disk2/liwu/taobao.basicQuery.txt"):
			term = term.strip().strip("\n").strip("\t")
			count = 0;
			while(count < 44):
				queryStr = search + term + "&s="+ str(count)
				yield Request(queryStr,meta={'query':term},callback=self.parse)
				#yield self.make_requests_from_url(queryStr,meta={'query':term})
				count += 44;

	def parse(self, response):
		query = response.meta['query']
		query = query.replace("\n","")
		for i in range(1,49):
			taobaoFile.write(str(i)+"\n");
			hxs = HtmlXPathSelector(response)
			img = hxs.select("//div[@class='item-box st-itembox']/div/p/a/span/img/@data-ks-lazyload")[i].extract();
			itemLink = hxs.select("//div[@class='item-box st-itembox']/h3[@class='summary']/a/@href")[i].extract()
			title= hxs.select("//div[@class='item-box st-itembox']/h3[@class='summary']/a/@title")[i].extract()
			storeName = hxs.select("//div[@class='item-box st-itembox']/div[@class='row']/div[@class='col seller feature-dsi-tgr']/a/text()")[i].extract()
			storeLink = hxs.select("//div[@class='item-box st-itembox']/div[@class='row']/div[@class='col seller feature-dsi-tgr']/a/@href")[i].extract()
			soldAmount= hxs.select("//div[@class='item-box st-itembox']/div[@class='row row-focus']/div[@class='col end dealing']/text()")[i].extract()
			price= hxs.select("//div[@class='item-box st-itembox']/div[@class='row row-focus']/div[@class='col price']/text()")[i].extract()
			taobaoFile.write(query)
			taobaoFile.write(seperatorChar)
			taobaoFile.write(img)
			taobaoFile.write(seperatorChar)
			taobaoFile.write(itemLink)
			taobaoFile.write(seperatorChar)
			taobaoFile.write(title.encode('utf8'))
			taobaoFile.write(seperatorChar)
			taobaoFile.write(storeName.encode('utf8'))
			taobaoFile.write(seperatorChar)
			taobaoFile.write(storeLink)
			taobaoFile.write(seperatorChar)
			taobaoFile.write(soldAmount.encode('utf8'))
			taobaoFile.write(seperatorChar)
			taobaoFile.write(price.encode('utf8'))
			taobaoFile.write("\n")
