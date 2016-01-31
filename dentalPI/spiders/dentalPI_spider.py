# -*- coding: utf-8 -*-
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from dentalPI.items import DentalpiItem
import re 
class PiSpider(CrawlSpider):
    name = "dentalpi"
    allowed_domains = ["dentistry.ucla.edu"]
    start_urls =["https://www.dentistry.ucla.edu/directory/faculty"]
    rules = [
        Rule(LinkExtractor(
    		allow=['/directory/faculty\?page=\d*','/directory/faculty$']),
    		callback='parse_item',
    		follow=True)
        ]

    def parse_item(self, response):
        
        selector_list = response.xpath('//div[@id="profileTeaserDetails"]')

        for selector in selector_list:
            item = DentalpiItem()
            pattern = re.compile(r'\n+\s*')
            pi_name = selector.xpath('div[1]/div[1]/h2/a/text()').extract()[0].strip()
            item['name'] = re.sub(pattern," ",pi_name)
            pi_title = "".join(selector.xpath('div[1]/div[2]/div/div/div/text()').extract())
            item['title'] = re.sub(pattern,", ",pi_title)[2:-2]
            item['email'] = selector.xpath('div[2]/div[1]/div/a/text()').extract()
            item['office'] = selector.xpath('div[2]/div[2]/div/text()[2]').extract()
            ext = selector.xpath('div[2]/div[3]/div/strong/text()').extract()
            pi_phone = "".join(selector.xpath('div[2]/div[3]/div/text()[1]').extract() + ext)
            item['phone'] = re.sub(pattern,"",pi_phone)
            
            
            yield item
                 

