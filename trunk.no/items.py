# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

class DoubanItem(Item):
    groupName = Field()
    groupURL = Field()
    totalNumber = Field()
    RelativeGroups = Field()
    ActiveUesrs = Field()

class QihooItem(Item):
    gameDetailURL = Field()

class AppchinaItem(Item):
    appchinaDetailURL = Field()

class MumayiItem(Item):
    mumayiDetailURL = Field()

class BaiduItem(Item):
    baiduDetailURL =  Field();

class TencentItem(Item):
    tencentDetailURL =  Field();

class QihooDetailItem(Item):
    icon = Field();
    gameName = Field();
    whichAppStroe = Field();
    star = Field();
    score = Field();
    downloadTimes = Field();
    updateTime = Field();
    freeOrMoney = Field();
    sizeMB = Field();
    gameVersion = Field();
    gameOS = Field();
    language = Field();
    classify =  Field();
    gameCompany = Field();
    hint360 = Field();
    images = Field();
