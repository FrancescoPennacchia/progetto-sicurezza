import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from urllib import request
import unicodedata
import os


import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from urllib import request
import unicodedata
import os


class MySpider(CrawlSpider):
    name = 'Spider-sicurezza'
    allowed_domains = ['addons.mozilla.org']
    start_urls = ['https://addons.mozilla.org/it/firefox/extensions/category/language-support/']

    rules = (
        Rule(LinkExtractor(restrict_css='.SearchResult-link'), callback='parse_item'),
        Rule(LinkExtractor(restrict_css='.Paginate-item--next')),
    )

    # Test normalization nomi con unicodedata
    def normalize_filename(self, name):
        # Rimuovi i caratteri non ASCII dal nome del file
        normalized_name = ''.join(c for c in name if unicodedata.category(c) != 'Mn')
        # Sostituisci i caratteri non consentiti con _
        return normalized_name

    def parse_item(self, response):
        title = response.css('.AddonTitle::text').get()
        download_link = response.css('.InstallButtonWrapper-download-link::attr(href)').get()

        if title and download_link:
            file_name = ' '.join(title.split()) + '.xpi'  # Aggiungi trattini tra i diversi spazi
            # file_name = self.normalize_filename(file_name)
            folder_path = 'language-support_2'  # Percorso della cartella di destinazione
            file_path = os.path.join(folder_path, file_name)  # Percorso completo del file di destinazione

            os.makedirs(folder_path, exist_ok=True)  # Crea la cartella se non esiste

            request.urlretrieve(download_link, file_path)
            self.log("File {file_name} scaricato correttamente nella cartella {folder_path}.")

        yield None
