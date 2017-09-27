# -*- coding: utf-8 -*-
#爬取糗百笑话
import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, Compose


class JokeItem(scrapy.Item):
    joke = scrapy.Field()


class JokeSpider(scrapy.Spider):
    name = 'joke'
    allowed_domains = ['qiushibaike.com']
    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0',
        'FEED_EXPORT_ENCODING':'utf-8',
        'ROBOTSTXT_OBEY':'False'}
    download_delay = 2.0
    start_urls = ['https://www.qiushibaike.com/text/page/{page}/'.format(page=page) for page in range(1,14)]

    def parse(self, response):
        for joke in response.xpath('//div[@class="content"]'):
          #  l = ItemLoader(item=JokeItem(), response=response, selector=joke)
         #   l.default_output_processor = Compose(TakeFirst(), lambda out: out.replace('\xa0', ''))
        #    l.add_xpath('joke', './/span/text()')
            temp = joke.xpath('.//span/text()')[0].extract().strip().replace('\r','')
            item = JokeItem()
            item['joke'] = temp
         #   item = l.load_item()
            yield item
            