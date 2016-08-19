#-*- coding:utf-8 –*-
from scrapy.selector import Selector
import os
import scrapy
from ..CommonUtil import  CommonUtil
from ..items import XiaohuaItem, SanWenItem
import time, datetime
site = 'http://www.sanwen.net'
maxdepth = 2;
util = CommonUtil();
domain = "www.sanwen.net";
acceptPre="http://www.sanwen.net";
class SanwenSpider(scrapy.Spider):
    name = "zhsw"
    allowed_domains = ["sanwen.net"]
    start_urls = (
        "http://www.sanwen.net",
        # "http://www.sanwen.net/subject/3854508/",
     )

    def parse(self, response):
        # self.parse_item(response);
        sel = Selector(response)
        count = 0;
        for link in sel.xpath('//a/@href').extract():
            if link.startswith("/"):
                link = site + link;
            if link.startswith(domain):
                link = "http://" + link;
            if link.startswith(acceptPre):
                isContinue = True;
            else:
                isContinue = False;
            fdep = util.getDep(response.url);
            if fdep is None:
                fdep = 1
            if isContinue and not util.hasUrl(link) and fdep <= maxdepth:
                util.saveUrl(link);
                util.saveDep(link, fdep+1);
                count += 1;
                request = scrapy.Request(link, callback=self.parse_url_item)
                yield request

    def parse_url_item(self, response):
        sel = Selector(response)
        count = 0;
        for link in sel.xpath('//a/@href').extract():
            if link.startswith("/"):
                link = site + link;
            if link.startswith(domain):
                link = "http://" + link;
            if link.startswith(acceptPre):
                isContinue = True;
            else:
                isContinue = False;
            fdep = util.getDep(response.url);
            if fdep is None:
                fdep = 1
            if isContinue and not util.hasUrl(link) and fdep <= maxdepth:
                util.saveUrl(link);
                util.saveDep(link, fdep + 1);
                count += 1;
                if (link.find("subject") != -1 or link.find("article") != -1) and link.find("list") == -1:
                    request = scrapy.Request(link, callback=self.parseData)
                else:
                    request = scrapy.Request(link, callback=self.parse_url_item)
                yield request

    def parse_item(self, response):
        try:
            print "response url:",response.url
            if response.url.startswith(acceptPre):
                item = self.parseData(response);
            return item
        except Exception as e:
            print e;
            return None

    def parseData(self, response):
        print "parse data:"+response.url
        sel = Selector(response)
        url = response.url
        belong = "";
        title = "";
        author = "";
        readNum = 0;
        content = "";
        try:
            belong = sel.xpath('//div[@class="subnav"]/a/text()').extract();
        except Exception as e:
            pass;
        print "belong:",belong

        try:
            sel.xpath('//h1/text()').extract()[0];
        except Exception as e:
            pass;
        print "title:", title
        # info = sel.xpath('//div[@class="info"]/text()').extract()[0];
        try:
            author = sel.xpath('//div[@class="info"]/a/text()').extract()[0];
            print "author:",author
        except Exception as e:
            pass;
        # readNum = sel.xpath('//span[@id="article_click"]/text()').extract();
        # print "readNum:",readNum

        try:
            contents = sel.xpath('//div[@class="content"]/p').extract();
            for c in contents:
                content = content + c;
        except Exception as e:
            pass;
        # date = "";
        # count = 0;
        # info = info.split(" ");
        # for ins in info:
        #     if(count == 0):
        #         date = ins;
        #     if(count == 1):
        #         date = date +" "+ins;
        #     if (count == 3):
        #         author = ins[ins.find(">")+1:];
        #     if (count == 4):
        #         readNum = ins;
        #     count = count + 1;

        # print belong,"\n",title,"\n",content,"\n",author
        if (len(content) > 10):
            item = SanWenItem();
            item['url'] = url
            item['belong'] = belong
            item['title'] = title
            item['read'] = readNum
            item['content'] = content
            item['author']=author
            ftime = time.localtime();
            y, m, d, h, mi, s = ftime[0:6]
            item['createAt'] = datetime.datetime(y, m, d, h, mi, s);
            item['updateAt'] = datetime.datetime(y, m, d, h, mi, s);
            item['publishAt'] = datetime.datetime(y, m, d, h, mi, s);
            item['checked'] = False;
            return item;

