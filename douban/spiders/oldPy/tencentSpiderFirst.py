from scrapy.contrib.spiders import  CrawlSpider, Rule
from scrapy.spider import BaseSpider
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from scrapy.item import Item
from douban.items import TencentItem 
import re

class AppchinaSpider(CrawlSpider):       
	name = "tencent"
	allowed_domains = ["myapp.com"]

	def start_requests(self):
		for i in range(1,2):
        		yield self.make_requests_from_url("http://android.myapp.com/android/game.jsp#cid=120&rank=0&pageno=%d" % i)

	rules = [
		Rule(SgmlLinkExtractor(allow=(r'.*')), callback='parse_group_home_page') ]

	def parse_group_home_page(self, response):
		self.log("Fetch group home page: %s" % response.url)
		#hxs = HtmlXPathSelector(response)
		item = TencentItem(); 
		item['tencentDetailURL'] = response.url
		return item
