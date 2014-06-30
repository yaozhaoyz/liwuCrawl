from scrapy.contrib.spiders import  CrawlSpider, Rule
from scrapy.spider import BaseSpider
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from scrapy.item import Item
from trunk.items import QihooItem 
import re

class QihooSpider(CrawlSpider):       
#CrawlSpider):
	name = "Qihoo"
	allowed_domains = ["360.cn"]
	#start_urls = [
	#	"http://zhushou.360.cn/game",
	#	"http://zhushou.360.cn/list/index/cid/2"
	#]

	def start_requests(self):
		for i in range(1,50):
        		yield self.make_requests_from_url("http://zhushou.360.cn/list/index/cid/2?page=%d" % i)


	rules = [
		Rule(SgmlLinkExtractor(allow=('/detail')), callback='parse_group_home_page') ]


	def parse_group_home_page(self, response):
		self.log("Fetch group home page: %s" % response.url)
		#hxs = HtmlXPathSelector(response)
		item = QihooItem()
		item['gameDetailURL'] = response.url
		return item
