import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class MySpider(CrawlSpider):
    name = 'my_spider'
    allowed_domains = ['addons.mozilla.org']
    start_urls = ['https://addons.mozilla.org/it/firefox/extensions/category/search-tools/']

    rules = (
        Rule(LinkExtractor(restrict_css='.SearchResult-link'), callback='parse_item'),
        Rule(LinkExtractor(restrict_css='.Paginate-item--next')),
    )

    def parse_item(self, response):
        download_link = response.css('.InstallButtonWrapper-download-link::attr(href)').get()
        # Esegui il download del file utilizzando il link ottenuto

        yield None
