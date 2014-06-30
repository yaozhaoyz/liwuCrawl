from scrapy.contrib.spiders import  CrawlSpider, Rule
from scrapy.spider import BaseSpider
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from scrapy.item import Item
from douban.items import BaiduItem 
import re

class AppchinaSpider(CrawlSpider):       
	name = "baidu"
	allowed_domains = ["baidu.com"]

	def start_requests(self):
		for i in range(1,100):
        		yield self.make_requests_from_url("http://as.baidu.com/a/asgame?cid=102&s=1&pn=%d" % i)

	rules = [
		Rule(SgmlLinkExtractor(allow=(r'http://as.baidu.com/a/item\?docid=')), callback='parse_group_home_page') ]

	def parse_group_home_page(self, response):
		self.log("Fetch group home page: %s" % response.url)
		#hxs = HtmlXPathSelector(response)
		item = BaiduItem(); 
		item['baiduDetailURL'] = response.url
		return item
