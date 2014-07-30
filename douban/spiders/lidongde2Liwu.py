from scrapy.contrib.spiders import  CrawlSpider, Rule
from scrapy.spider import BaseSpider
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from scrapy.http import FormRequest
from scrapy.http import Request
from scrapy.item import Item
from urllib import quote
import re
import sys  
import datetime

reload(sys)  
sys.setdefaultencoding('utf8')   

now = datetime.datetime.now()
nowday = now.strftime("%Y%m%d")
fileIn = open("/disk2/liwu/lidongde/lidongde.first.txt","r");
fileOutliwu = open("/disk2/liwu/lidongde/2liwu_"+nowday,'w');
fileOutgohao= open("/disk2/liwu/lidongde/2gohao_"+nowday,'w');
tempOut = open("/disk2/liwu/lidongde/tmp",'w');

class liwuSpider(CrawlSpider):	   
	name = "lidongde2liwu"
	allowed_domains = ["lidongde.com"]

	def start_requests(self):
		for line in fileIn: 
			tempOut.write("aa"+line+"\n")
			try:
				a,b,c,d,e = line.strip().split("\"");
			except:
				continue;
			i = 0;
			while(i<15):
				i += 1 
				url = d + "?p=" + str(i);
				tempOut.write("uu"+url+"\n")
				yield self.make_requests_from_url(url);

	def parse(self,response):
		if(response.url.find("http://www.lidongde.com/liwu")>=0):
			yield self.parseLiwu(response);
		elif (response.url.find("http://www.lidongde.com/gohao")>=0):
			yield self.parseGohao(response);
			
	def parseGohao(self,response):
		hxs= HtmlXPathSelector(response)
		url = response.url
		pageTitle = hxs.select("/html/head/title/text()")[0].extract();
		i = 0;
		while(i<20): 
			i+= 1;
			try:
				title = hxs.select("/html/body/div[2]/div[3]/div/div/div[2]/a/text()")[i].extract();
				#href = hxs.select("/html/body/div[2]/div[3]/div/div/div[2]/a/@href")[i].extract();
				#href = "http://www.lidongde.com"+href;
				#img = hxs.select("/html/body/div[2]/div[3]/div/div/div[2]/a/img/@src")[i].extract();
				#img = "http://www.lidongde.com"+img;
				#price = hxs.select("/html/body/div[2]/div[3]/div/div/div[2]/span/text()")[i].extract();
				tags = "" 
				price = "" 
				desc = "" 
				fileOutgohao.write(pageTitle+"\t"+url);
				#fileOutgohao.write(pageTitle+"\t"+url+"\t"+title+"\t"+href+"\t"+tags+"\t"+price+"\t"+desc+"\t"+img+"\n");
			except:
				continue;
		return ;

	def parseLiwu(self, response):
		hxs = HtmlXPathSelector(response)
		url = response.url
		pageTitle = hxs.select("/html/head/title/text()")[0].extract();
		i = 0;
		while(i<5): 
			i+= 1;
			try:
				title = hxs.select("/html/body/div[2]/div[3]/div[1]/div[@class='list_box']/div[@class='list_box_con']/div[@class='list_box_tit']/a/text()")[i].extract();
				href = hxs.select("/html/body/div[2]/div[3]/div[1]/div[@class='list_box']/div[@class='list_box_con']/div[@class='list_box_tit']/a/@href")[i].extract();
				href = "http://www.lidongde.com"+href;
				tags = hxs.select("/html/body/div[2]/div[3]/div[1]/div[@class='list_box']/div[@class='list_box_con']/div[@class='list_box_inf']/text()")[i].extract();
				price = hxs.select("/html/body/div[2]/div[3]/div[1]/div[@class='list_box']/div[@class='list_box_con']/div[@class='list_box_inf']/span/text()")[i].extract();
				desc = hxs.select("/html/body/div[2]/div[3]/div[1]/div[@class='list_box']/div[@class='list_box_con']/div[@class='list_box_des']/text()")[i].extract();
				img = hxs.select("/html/body/div[2]/div[3]/div[1]/div[@class='list_box']/div[@class='list_box_con']/div[@class='list_box_pic fr']/img/@src")[i].extract();
				img = "http://www.lidongde.com"+img;
				fileOutliwu.write(pageTitle+"\t"+url+"\t"+title+"\t"+href+"\t"+tags+"\t"+price+"\t"+desc+"\t"+img+"\n");
			except:
				continue;
		return ;
