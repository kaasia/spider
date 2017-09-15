#爬取豆瓣top250部电影信息
# -*- coding: utf-8 -*-
import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, Compose


class MovieItem(scrapy.Item):
    title = scrapy.Field()
    link = scrapy.Field()
    rating_num = scrapy.Field()
    rating_people = scrapy.Field()
    quote = scrapy.Field()


class MovieSpider(scrapy.Spider):
    name = 'movie_250'
    allowed_domains = ['movie.douban.com']
    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0',
        'FEED_EXPORT_ENCODING':'utf-8',
        'ROBOTSTXT_OBEY':'False'}
    download_delay = 2.0
    start_urls = ['https://movie.douban.com/top250']

    def parse(self, response):
        for movie in response.xpath('//div[@class="item"]'):
            l = ItemLoader(item=MovieItem(), response=response, selector=movie)
            l.default_output_processor = Compose(TakeFirst(), lambda out: out.replace('\xa0', ''))
            l.add_xpath('title', 'normalize-space(.//div[@class="hd"])')
            l.add_xpath('link', './/div[@class="hd"]/a/@href')
            l.add_xpath('rating_num', './/span[@class="rating_num"]/text()')
            l.add_xpath('rating_people', './/text()[contains(., "人评价")]')
            l.add_xpath('quote', './/span[@class="inq"]/text()')
            item = l.load_item()
            yield item
            
        for next_page in response.xpath('//span[@class="next"]/a'):
            yield response.follow(next_page, self.parse)
