from scrapy.contrib.spiders import  CrawlSpider, Rule
from scrapy.spider import BaseSpider
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from scrapy.item import Item
from trunk.items import AppchinaItem 
import re

class AppchinaSpider(CrawlSpider):       
#CrawlSpider):
	name = "appchina"
	allowed_domains = ["appchina.com"]

	def start_requests(self):
		for i in range(1,100):
        		yield self.make_requests_from_url("http://www.appchina.com/category/40/1_1_%d_1_0_0_0.html" % i)

	rules = [
		Rule(SgmlLinkExtractor(allow=('/app')), callback='parse_group_home_page') ]

	def parse_group_home_page(self, response):
		self.log("Fetch group home page: %s" % response.url)
		#hxs = HtmlXPathSelector(response)
		item = AppchinaItem(); 
		item['appchinaDetailURL'] = response.url
		return item
