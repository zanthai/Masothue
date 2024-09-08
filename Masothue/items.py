# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class MasothueItem(scrapy.Item):
    tencty = scrapy.Field()
    tenqt = scrapy.Field()
    masothue = scrapy.Field()
    diachi = scrapy.Field()
    nguoidaidien = scrapy.Field()
    phone = scrapy.Field()
    ngayhoatdong = scrapy.Field()
    quanly = scrapy.Field()
    loaihinh = scrapy.Field()
    tinhtrang = scrapy.Field()
    courseUrl = scrapy.Field() 
    coursename = scrapy.Field()