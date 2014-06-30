from scrapy.contrib.spiders import  CrawlSpider, Rule
from scrapy.spider import BaseSpider
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from scrapy.item import Item
from douban.items import MumayiItem 
import re

class MumayiSpider(CrawlSpider):       
	name = "mumayi"
	allowed_domains = ["mumayi.com"]

	def start_requests(self):
		for i in range(1,20):
        		yield self.make_requests_from_url("http://www.mumayi.com/android/qipaitiandi/list_33_%d.html" % i)
		for i in range(1,20):
        		yield self.make_requests_from_url("http://mpk.mumayi.com/tiyv-download-%d.html" % i)
		for i in range(1,20):
        		yield self.make_requests_from_url("http://mpk.mumayi.com/yizhi-download-%d.html" % i)
		for i in range(1,20):
        		yield self.make_requests_from_url("http://mpk.mumayi.com/saiche-download-%d.html" % i)
		for i in range(1,20):
        		yield self.make_requests_from_url("http://mpk.mumayi.com/feixing-download-%d.html" % i)
		for i in range(1,20):
        		yield self.make_requests_from_url("http://mpk.mumayi.com/qipai-download-%d.html" % i)
		for i in range(1,20):
        		yield self.make_requests_from_url("http://mpk.mumayi.com/yangcheng-download-%d.html" % i)
		for i in range(1,20):
        		yield self.make_requests_from_url("http://mpk.mumayi.com/dongzuo-download-%d.html" % i)
		for i in range(1,20):
        		yield self.make_requests_from_url("http://mpk.mumayi.com/jiaose-download-%d.html" % i)
		for i in range(1,20):
        		yield self.make_requests_from_url("http://mpk.mumayi.com/game-download-2.html" % i)

	rules = [
		Rule(SgmlLinkExtractor(allow=(r'http://www.mumayi.com/android-\d+.html')), callback='parse_group_home_page'), 
		Rule(SgmlLinkExtractor(allow=(r'/\d+.html')), callback='parse_group_home_page') ]

	def parse_group_home_page(self, response):
		self.log("Fetch group home page: %s" % response.url)
		#hxs = HtmlXPathSelector(response)
		item = MumayiItem(); 
		item['mumayiDetailURL'] = response.url
		return item
