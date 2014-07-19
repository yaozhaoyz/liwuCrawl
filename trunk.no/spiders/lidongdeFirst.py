from scrapy.contrib.spiders import  CrawlSpider, Rule
from scrapy.spider import BaseSpider
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from scrapy.item import Item
from trunk.items import QihooItem 
import re

class lidongdeSpider(CrawlSpider):       
#CrawlSpider):
	name = "lidongde"
	allowed_domains = ["lidongde.com"]

	def start_requests(self):
        yield self.make_requests_from_url("http://www.lidongde.com/liwu")

	rules = [
		Rule(SgmlLinkExtractor(allow=('/\w*')), callback='parse_group_home_page') ]

	def parse_group_home_page(self, response):
		self.log("Fetch group home page: %s" % response.url)
		#hxs = HtmlXPathSelector(response)
		item = Item()
		item['songliduixiang'] = response.url
		return item
