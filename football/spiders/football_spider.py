import scrapy
from scrapy.exceptions import DropItem
from football.items import FootballItem

class FootballSpider(scrapy.Spider):
    name = "football"
    allowed_domains = ["premierleague.com"]
    start_urls = [
        "http://www.premierleague.com/content/premierleague/en-gb/matchday/results.html?paramClubId=ALL&paramComp_8=true&view=.dateSeason&paramSeasonId=2015",
        "http://www.premierleague.com/content/premierleague/en-gb/matchday/results.html?paramClubId=ALL&paramComp_8=true&view=.dateSeason&paramSeasonId=2014",
        "http://www.premierleague.com/content/premierleague/en-gb/matchday/results.html?paramClubId=ALL&paramComp_8=true&view=.dateSeason&paramSeasonId=2013",
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
        #season = response.xpath('//select[@id="season"]/option[@selected="selected"]/text()').extract()
        season = response.xpath('//div[@class="fixtures-container fixturelist"]/div/h2/text()').extract()
        for dates in response.xpath('//table[@class="contentTable"]/tbody'):
            date = dates.xpath('tr/th/text()').extract()
            for sel in dates.xpath('tr[position()>1]'):
                item = FootballItem()
                item['season'] = [i.split()[1] for i in season]
                item['date'] = date
                item['time'] = [i.split()[0] for i in sel.xpath('td[@class="time"]/text()').extract()]
                item['location'] = sel.xpath('td[@class="location"]/a/text()').extract()
                item['home'] = sel.xpath('td[@class="clubs rHome"]/a/text()').extract()
                item['homescore'] = [i.split()[0] for i in sel.xpath('td[@class="clubs score"]/a/text()').extract()]
                item['awayscore'] = [i.split()[2] for i in sel.xpath('td[@class="clubs score"]/a/text()').extract()]
                item['away'] = sel.xpath('td[@class="clubs rAway"]/a/text()').extract()
                yield item