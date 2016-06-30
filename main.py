import scrapy
import sys

teams = []
players = []

class BlogSpider(scrapy.Spider):
    name = 'blogspider'
    start_urls = ['http://www.scoutscartola.com/clube']

    def parse(self, response):
        for team_link in response.xpath("//div[@class='bloco']/a")  :
            # for team_name in team_link.xpath('./text()').extract():
            #     teams.append(team_name)
            for link in team_link.xpath('./@href').extract():
                yield scrapy.Request(response.urljoin(link), self.get_players)

    def get_players(self, response):
        for player in response.xpath("//p[@class='atleta']/a[@class='atletalink']/text()").extract():
            print(player)
            sys.stdin.read(1)
