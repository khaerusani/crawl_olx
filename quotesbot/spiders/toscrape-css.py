# -*- coding: utf-8 -*-
import re
import scrapy
from os import write, close
from tweepy.streaming import json


class ToScrapeCSSSpider(scrapy.Spider):
    name = "toscrape-css"
    start_urls = [
        'http://olx.co.id/elektronik-gadget/handphone/samsung/',
    ]

    def parse(self, response):
        for quote in response.css("li.tleft"):
            text = [i.split('\t\t\t\t\t\t',1)[1] for i in (quote.css("a.link > span").extract())]
            harga = [i.split('\t\t\t',1)[1] for i in (quote.css("p.price > strong.c000").extract())]
            data = {}
            data['olx'] = []
            data['olx'].append({
                'text' : [a.split('\t',1)[0] for a in text],
                'harga' : [a.split('\t',1)[0] for a in harga],
                'link': quote.css("a.link::attr(href)").extract()})
            with open('data.json', 'a') as outfile:
                json.dump(data, outfile, indent=2)
                print(str(data['olx'])+" Saved To Json")
        next_page_url = response.css("span.fbold > a::attr(href)").extract_first()
        next = re.search('\S+\=', next_page_url).group(0)
        i=1
        while (next is not None) and (i<500):
            j = str(i)
            yield scrapy.Request(response.urljoin(next+j))
            i+=1
