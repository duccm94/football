import scrapy
from scrapy.exceptions import DropItem
from football.items import FootballItem

class FootballSpider(scrapy.Spider):
    name = "football"
    allowed_domains = ["premierleague.com"]
    start_urls = [
        "http://www.premierleague.com/en-gb/matchday/results.html?paramComp_100=true&view=.dateSeason.html?paramComp_8=true",
    ]

    def start_requests(self):
            for url in self.start_urls:
                yield scrapy.Request(url, self.parse, meta={
                    'splash': {
                        'endpoint': 'render.html',
                        'args': { 'wait': 0.5 }
                    }
                })

    def parse(self, response):
        for dates in response.xpath('//table[@class="contentTable"]/tbody'):
            date = dates.xpath('tr/th/text()').extract()
            for sel in dates.xpath('''set:difference(.//tr,.//tr/th)'''):
                item = FootballItem()
                item['date'] = date
                item['time'] = sel.xpath('td[@class="time"]/text()').extract()
                item['time'] = [i.split()[0] for i in item['time']]
                item['location'] = sel.xpath('td[@class="location"]/a/text()').extract()
                item['home'] = sel.xpath('td[@class="clubs rHome"]/a/text()').extract()
                item['homescore'] = sel.xpath('td[@class="clubs score"]/a/text()').extract()
                item['homescore'] = [i.split()[0] for i in item['homescore']]
                item['awayscore'] = sel.xpath('td[@class="clubs score"]/a/text()').extract()
                item['awayscore'] = [i.split()[2] for i in item['awayscore']]
                item['away'] = sel.xpath('td[@class="clubs rAway"]/a/text()').extract()
                if item['time']:
                    yield item