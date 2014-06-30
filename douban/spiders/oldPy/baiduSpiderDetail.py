from scrapy.contrib.spiders import  CrawlSpider, Rule
from scrapy.spider import BaseSpider
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from scrapy.http import FormRequest
from scrapy.http import Request
from scrapy.item import Item
from urllib import quote
from douban.items import BaiduItem 
import re
import sys  
reload(sys)  
sys.setdefaultencoding('utf8')   

detailURLs = "FirstURLs/baidu.json1";
tempOUT = open("baiduResult/out.detail",'w');
tempOUT2 = open("baiduResult/out.validOrNot",'w');

class BaiduDSpider(CrawlSpider):	   
	name = "BaiduDetail"
	DOWNLOAD_DELAY = 1.0
	allowed_domains = ["baidu.com"]

	def start_requests(self):
		for line in open(detailURLs):
			try:
				a,b,c,d,e = line.strip().split("\"");
			except:
				continue;
			tempOUT2.write("\n"+d+"\t");
			tempOUT.write("\007"+d+"\001");	
			yield self.make_requests_from_url(d);

	def parse(self, response):
		try:
			hxs = HtmlXPathSelector(response)
			iconURL = hxs.select("//dt[@class='fleft']")[0].extract();
			gameName = hxs.select("//span[@id='appname']")[0].extract();
			commentStar = hxs.select("//*[@id='score-num']")[0].extract();
			commentScore = commentStar;
			sizeMB = hxs.select("//span[@class='params-size']")[0].extract();
			gameOS = hxs.select("//span[@class='params-platform']")[0].extract();
			gameVersion = hxs.select("//span[@class='params-vname']")[0].extract();
			downloadTimes = hxs.select("//span[@class='params-download-num']")[0].extract();
			updateTime = hxs.select("//span[@class='params-updatetime']")[0].extract();
			downloadURL = hxs.select("//*[@id='down_as_durl']")[0].extract();
			gameImages_1 = hxs.select("//ul[@class='screen cls data-screenshots']/li[1]/img").extract();
			gameImages_2 = hxs.select("/html/body/div[5]/div[3]/div[1]/div[2]/div[2]/div[2]/div[1]/ul/li[2]/img").extract();
			gameImages_3 = hxs.select("/html/body/div[5]/div[3]/div[1]/div[2]/div[2]/div[2]/div[1]/ul/li[3]/img").extract();
			gameImages_4 = hxs.select("/html/body/div[5]/div[3]/div[1]/div[2]/div[2]/div[2]/div[1]/ul/li[4]/img").extract();
			gameImages_5 = hxs.select("/html/body/div[5]/div[3]/div[1]/div[2]/div[2]/div[2]/div[1]/ul/li[5]/img").extract();
			gameImages_6 = hxs.select("/html/body/div[5]/div[3]/div[1]/div[2]/div[2]/div[2]/div[1]/ul/li[6]/img").extract();
			freeOrMoney = hxs.select("//dt[@class='fleft']/p").extract()[0]; 
			tempOUT.write("yes"+gameImage_1);
			Classify = hxs.select("/html/body/div[5]/div[1]/span[5]/a").extract();
			Description = hxs.select("//div[@class='brief-des']")[0].extract();
			tempOUT.write(""+iconURL+"\001"+gameName+"\001"+commentStar+"\001"+commentScore+"\001"+downloadTimes+"\001"+updateTime+"\001"+freeOrMoney);#+"\001"+sizeMB+"\001"+gameVersion);#+"\001"+gameOS+"\001"+Classify+"\001"+Description+"\001"+gameImages_1+"\001"+downloadURL);
			for i in range(1,10):
				yield Request(comment_url,meta={'url':"baiduResult/dt_"+gameName, 'comment_id':i},callback=self.parse_stores)
		except:
			tempOUT2.write("hxs error!");
			return;

	def parse_stores(self, response):
		thisURL = response.meta['url'];
		f_id = response.meta['comment_id'];
		thisOUT = open(""+thisURL+".comment."+f_id,'w');
		thisOUT.write("\001"+response.body+"\006");
		tempOUT.write("\001"+response.body+"\006");
