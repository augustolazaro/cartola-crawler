import scrapy
import urlparse

class Player(scrapy.Item):
    name = scrapy.Field()
    link = scrapy.Field()
    team = scrapy.Field()
    position = scrapy.Field()

class ScoutsCartola(scrapy.Spider):
    name = 'scouts-cartola'

    def __init__(self, tag=None):
        teams_url = 'http://www.scoutscartola.com'

        self.start_urls = [teams_url + '/jogador']

    def parse(self, response):
        build_full_url = lambda link: urlparse.urljoin(response.url, link)

        for player in response.css("#boxAlfabetica > a"):
            it = Player()

            it['name'] = player.xpath('text()')[0].extract()
            it['link'] = build_full_url(player.xpath('@href')[0].extract())

            return [scrapy.Request(it['link'], callback=self.parse_player, meta={'player': it})]


    def parse_player(self, response):
        player = response.meta['player']

        links = []

        for mainData in response.css("#bloco2 > div > a"):
            links.append(mainData.xpath('text()')[0].extract())

        player['team'] = links[0]
        player['position'] = links[2]

        yield player
