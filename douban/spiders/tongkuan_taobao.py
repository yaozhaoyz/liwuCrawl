#coding=utf-8
from scrapy.spider import BaseSpider
from scrapy.contrib.spiders import  CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from scrapy.http import FormRequest
from scrapy.http import Request
from scrapy.item import Item
from urllib import *
import json
import sys;
import re
import time 
import datetime

import commands,datetime,os,time

today=datetime.date.today().strftime("%Y-%m-%d")
yesterday=(datetime.date.today()-datetime.timedelta(days=1)).strftime("%Y-%m-%d")
basicPath='/disk2/liwu/tongkuanData/output/'
basicPathIn ='/disk2/liwu/tongkuanData/input/.tongkuan.out.new'
commands.getstatusoutput('mkdir -p '+basicPath)
basicPathOut=open(basicPath+"tongkuan.txt","a")
dumpPathOut=open(basicPath+"dumpItemInfo.txt","a")
tmallPriceOut=open(basicPath+"tmallPrice.txt","a")

class taobaoTongkuanSpider(CrawlSpider):       
#CrawlSpider):
    name = "taobaoTongkuan"
    headers = {
    "Accept": "*/*",
    "Accept-Encoding": "gzip,deflate",
    "Accept-Language": "en-US,en;q=0.8,zh-TW;q=0.6,zh;q=0.4",
    "Connection": "keep-alive",
    "Content-Type":" application/x-www-form-urlencoded; charset=UTF-8",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.111 Safari/537.36",
    "Referer": "http://www.taobao.com/"
    }

    def start_requests(self):
        for line in open(basicPathIn):
            termA = line.split('\t')
            time.sleep(10)
            tid = termA[0].strip();
            url = termA[1].strip()
            img = termA[2].strip();
            sId=termA[3].strip();
            yield Request(url,meta={'tid':tid,'url':url,'img':img,'sId':sId},cookies={"thw":"cn","cna":"345ODXZQzU0CAXrh3uOZ174E","v":"0","uc3":"nk2","existShop":"MTQyMjM3MzkyMw%3D%3D","unt":"yaozhaoyz%26center","lgc":"yaozhaoyz","tracknick":"yaozhaoyz","sg":"z75","_cc_":"UIHiLt3xSw%3D%3D","tg":"0","_l_g_":"Ug%3D%3D","cainiao_abtest9_1":"1","_tb_token_":"9NpFLenyeje5","cookie2":"1e4bb0e545ff1ce869db709da105469f","cookie1":"BxeCj6gUGdxjG6Oq8g%2F38557GDuii7lyae%2Feuh1sqGQ%3D","unb":"402436137","mt":"ci","t":"a3f4ff6bc91d0ba9a38c4906fef95e19","_nk_":"yaozhaoyz","cookie17":"VyyTnRdd0GYK","isg":"F6EB8C012141054C8093D1EF01FA93D1","uc1":"lltime"},callback=self.parse)
        return ;
    
    def parse(self, response):
        url = response.meta['url']
        tid = response.meta['tid']
        img = response.meta['img']
        sId = response.meta['sId']
        hsx = HtmlXPathSelector(response)
        title = ""
        sellAmount = "";
        price = "";
        ori_price = ""
        isTmall = "1"
        #print response.body;
        if url.find("http://item.taobao.com")==0:
            isTmall = "0"
            try:
                title = hsx.xpath("//h3[@class='tb-main-title']/@data-title")[0].extract().strip();
                ori_price = hsx.xpath('//div[@class="tb-property-cont"]/strong/em[2]/text()')[0].extract()
                price = hsx.xpath('//strong[@id="J_StrPrice"]/em[2]/text()')[0].extract()
                img = hsx.xpath('//img[@id="J_ImgBooth"]/@data-src')[0].extract()
                img = img.replace("_400x400","_100x100");
            except:
                img = response.meta['img']; 
                print "parse taobao error " + str(tid)+":"+url;
        if url.find("http://detail.tmall.com/")==0:
            isTmall = "1"
            try:
                title = hsx.xpath("//div[@class='tb-detail-hd']/h1/text()")[0].extract().strip()
                ori_price = "";
                price = "";
                try:
                    ori_price = hsx.xpath('//dl[@class="tm-price-panel"]/dd/span/text()')[0].extract()
                    ori_price = ori_price.split('-')[0]
                    price = hsx.xpath('//div[@class="tm-promo-price"]/span/text()')[0].extract()
                except:
                    ori_price = "";
                    price = ""; 
                    mdsQueryStr="http://mdskip.taobao.com/core/initItemDetail.htm?itemId="+sId
                    refer = "http://detail.tmall.com/item.htm?id="+sId
                    yield Request(mdsQueryStr,headers={'Referer':refer},meta={'sId':sId},callback=self.parseTmallPrice)
                img = hsx.xpath('//img[@id="J_ImgBooth"]/@src')[0].extract()
                img = img.replace("_400x400","_100x100");
            except:
                img = response.meta['img']; 
                print "parse tmall  error " + str(tid)+":"+url;
        if title!="":
            queryStr="http://s.m.taobao.com/search?event_submit_do_new_search_auction=1&_input_charset=utf-8&topSearch=1&atype=b&searchfrom=1&action=home%3Aredirect_app_action&from=1&sst=1&n=20&buying=buyitnow&m=api4h5&abtest=1&wlsort=1&style=list&closeModues=nav%2Cselecthot%2Conesearch&callback=json&q="+quote(title.encode("utf8")); 
            yield Request(queryStr ,meta={'isTmall':isTmall,'title':title,'sId':sId, 'tid':tid,'queryStr':queryStr,'img':img, 'price':price,'ori_price':ori_price,'url':url},callback=self.parseDetail)

    def parseTmallPrice(self,response):
        jsonStr = str(response.body);
        #print jsonStr;
        sId = response.meta['sId']
        regStr = re.compile('"priceInfo":(.*?)]')
        regResList = regStr.findall(jsonStr);
        if len(regResList)>=1:
            try:    
                regRes = regResList[0]
                a = regRes.find(":");
                regRes1  = regRes[a+1:];
                regRes2 = regRes1+"]}";
                print regRes2;
                jsonMap = {}
                try:
                    jsonMap =  json.loads(regRes2,encoding="gbk")
                except ValueError, e:
                    print e;
                price = jsonMap["price"]
                ori_price = jsonMap["price"]
                try:
                    proList = jsonMap["promotionList"][0]
                    ori_price = proList["price"]
                except:
                    ori_price = jsonMap["price"]
                tmallPriceOut.write(str(sId)+"\t"+str(price)+"\t"+str(ori_price)+"\n");
            except:
                jsonStr = str(response.body);

    def parseDetail(self,response):
        query = response.meta['queryStr']
        tid = response.meta['tid']
        title = response.meta['title']
        bImg = response.meta['img']
        bPrice= response.meta['price']
        bOriPrice= response.meta['ori_price']
        bUrl = response.meta['url']
        sId = response.meta['sId'] 
        bisTmall = response.meta['isTmall'] 
        bLevel = "-1"
        bSource = "1"
        if bisTmall == "1":
            bLevel = "00"
            bSource = "2" 
        bSoldAmount = "0";
        basicPathOut.write(tid+"\t")
        basicPathOut.write(title.encode("utf8"))
        basicPathOut.write("\t"+bImg+"\t"+bPrice+"\t"+bOriPrice+"\t"+bLevel+"\t"+bUrl+"\t"+str(bSoldAmount)+'\t1\t'+bSource +"\n");
        jsonStr = str(response.body);
        ind = jsonStr.find("json(");
        jsonStr = jsonStr[ind+5:]
        jsonStr = jsonStr.rstrip(");</pre>");
        jsonMap=  json.loads(jsonStr)
        if( "errorCode" in jsonMap and jsonMap["errorCode"] == "1"):
            return None 
        if( "result" in jsonMap and jsonMap["result"] != "true"):
            return None 
        jsonList = jsonMap["listItem"];
        for item in jsonList:
            bSelf = "0"; # not self
            title =  item["name"].encode("utf8")
            img = item["img2"]+"_100x100.jpg"
            price = item["price"]
            ori_price = item['originalPrice']
            isTmall = item['userType'] 
            level = "-1"
            source = "2" # 1 tmall; 2 taobao. 3 .jd
            if isTmall=="1":
                level="00"
                source = "1"
            numId = item['itemNumId']
            if numId == sId:
                bSelf = "1"
            url = "http://item.taobao.com/item.htm?id="+numId 
            if isTmall == "1":
                url = "http://detail.tmall.com/item.htm?id="+numId
            soldAmount = item["act"]
            if tid != "" and numId != "": 
                basicPathOut.write(tid+"\t")
                #basicPathOut.write(sId+"\t")
                basicPathOut.write(title)
                basicPathOut.write("\t"+img+"\t"+price+"\t"+ori_price+"\t"+level+"\t"+url+"\t"+str(soldAmount)+"\t"+ bSelf +"\t"+source+"\n");
                basicPathOut.flush()

