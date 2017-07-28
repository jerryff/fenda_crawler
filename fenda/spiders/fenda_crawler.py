# -*- coding: utf-8 -*-
import scrapy
import json
from fenda.config import UsersConfig
from fenda.items import LiveItem
from fenda.items import CommentItem

class LiveSpider(scrapy.Spider):
    name = "fenda"

    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "zh-CN,zh;q=0.8",
        "Connection": "keep-alive",
        "Host": "fd.zaih.com",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
        "authorization": "oauth 8274ffb553d511e6a7fdacbc328e205d",
        "x-api-version": "3.0.55"
    }

    relay_headers = {
        "Accept" : "*/*",
        "Accept-Encoding" : "gzip, deflate, sdch, br",
        "Accept-Language" : "en,zh-CN;q=0.8,zh;q=0.6,zh-TW;q=0.4",
        "Access-Control-Request-Headers" : "authorization,x-api-version",
        "Access-Control-Request-Method": "GET",
        "Connection" : "keep-alive",
        "Host":"fd.zaih.com",
        "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
    }

    def __init__(self):
        pass

    def start_requests(self):
        count = 0
        while True:
            if count>=40:
                break
            count+=1
            currentUrl = "http://fd.zaih.com/api/v1/tags/10/accounts?page="+str(count)+"&per_page=20"
            yield scrapy.Request(
                url= currentUrl,
                headers= self.headers,
                meta = {
                    'proxy': UsersConfig['proxy'],
                    'from': {
                        'sign': 'else',
                        'data': {}
                    }
                },
                callback = self.monthly_live,
                dont_filter = True
            )

    def monthly_live(self, response):
        json_results = json.loads(response.body)

        if len(json_results)>0:
            yield LiveItem(data=json_results, type="speech")

            for each in json_results:
                nextPage = "http://fd.zaih.com/tutor/" + str(each["id"])

                yield scrapy.Request(
                    url= nextPage,
                    headers= self.headers,
                    meta = {
                        'id': each["id"],
                        'proxy': UsersConfig['proxy'],
                        'from': {
                            'sign': 'else',
                            'data': {}
                        }
                    },
                    callback = self.live_comment,
                    dont_filter = True
                )

    def live_comment(self, response):
        data=[]
        data.append(response.xpath('//meta[@name="pageData"]//@content').extract())
        # data.append(response.xpath("//div[@class=\"title\"]/text()"))
        # data.append(response.xpath("//title/text()"))
        
        yield CommentItem(data=data, type="comment", id=response.meta["id"])
