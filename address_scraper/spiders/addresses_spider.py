import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors.sgml import SgmlLinkExtractor
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import HtmlXPathSelector
import logging
from ..items import ZillowItem
from scrapy.http import Request, HtmlResponse
import csv 

class addressesSpider(scrapy.Spider) :
    name = "addresses"
    allowed_domains = ["zillow.com"]
    start_urls = ['https://www.zillow.com/ca/fsbo/']

    def parse(self, response):
        for listing in response.xpath(
                '//div[@id="search-results"]//ul[@class="photo-cards"]/li//a[contains(@href, "homedetails")]/@href'):
            listing = listing.extract()
            url = response.urljoin(listing.strip())
            yield Request(url, callback=self.parse_item)

    def parse_item(self, response):
        address = response.xpath('//header[@class="zsg-content-header addr"]/h1/text()').extract()

        if address:
            item = ZillowItem()

            itemprop_address = response.xpath('//span[@itemprop="address"]')
            addr = response.xpath('//span[@itemprop="streetAddress"]/text()').extract()
            addr = addr[0].strip() if addr else None
            city = response.xpath('//span[@itemprop="addressLocality"]/text()').extract()
            city = city[0].strip() if city else None
            state = response.xpath('//span[@itemprop="addressRegion"]/text()').extract()
            state = state[0].strip() if state else None

            item['addr'] = addr
            item['city'] = city
            item['state'] = state

            return item

        else:
            return None


