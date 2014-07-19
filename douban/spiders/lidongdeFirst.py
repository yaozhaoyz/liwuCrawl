from scrapy.contrib.spiders import  CrawlSpider, Rule
from scrapy.spider import BaseSpider
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from scrapy.item import Item
from douban.items import AItem 
import re

class lidongdeSpider(CrawlSpider):	   
#CrawlSpider):
	name = "lidongde"
	allowed_domains = ["lidongde.com"]

	def start_requests(self):
		yield self.make_requests_from_url("http://www.lidongde.com/")
		yield self.make_requests_from_url("http://www.lidongde.com/gohao")

	rules = [
		Rule(SgmlLinkExtractor(allow=('/liwu/[a-zA-Z]+')), callback='parse_group_home_page'), 
		Rule(SgmlLinkExtractor(allow=('/gohao/[a-zA-Z]+')), callback='parse_group_home_page') ]

	def parse_group_home_page(self, response):
		self.log("Fetch group home page: %s" % response.url)
		#hxs = HtmlXPathSelector(response)
		if( (response.url.find("http://www.lidongde.com/liwu")>=0)or(response.url.find("http://www.lidongde.com/gohao")>=0) ):
			item = AItem()
			item['URL'] = response.url
		return item
