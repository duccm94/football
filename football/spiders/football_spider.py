import scrapy

from football.items import FootballItem

class FootballSpider(scrapy.Spider):
    name = "football"
    allowed_domains = ["www.premierleague.com"]
    start_urls = [
        "http://www.premierleague.com/content/premierleague/en-gb/matchday/results.html?paramClubId=ALL&paramComp_8=true&paramSeasonId=2015&view=.dateSeason",
    ]

    def parse(self, response):
        for sel in response.xpath('//table[@class="contentTable"]/tbody'):
            item = FootballItem()
            item['date'] = sel.xpath('tr/th/text()').extract()
            item['time'] = sel.xpath('tr/td[@class="time"]/text()').extract()
            item['location'] = sel.xpath('tr/td[@class="location"]/a/text()').extract()
            item['home'] = sel.xpath('tr/td[@class="clubs rHome"]/a/text()').extract()
            item['homescore'] = sel.xpath('tr/td[@class="clubs score"]/a/text()').extract()
            item['awayscore'] = sel.xpath('tr/td[@class="clubs score"]/a/text()').extract()
            item['away'] = sel.xpath('tr/td[@class="clubs rAway"]/a/text()').extract()
            yield item