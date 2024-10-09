import scrapy
from scrapy.http import Request
import time
import os
from href.items import HtmlContentItem  # Import the item class

class ConstellationScraper(scrapy.Spider):
    name = 'constellation_href'
    start_urls = ['https://www.constellationenergy.com/']

    visited_urls = set()

    def start_requests(self):
        self.start_time = time.time()
        for url in self.start_urls:
            yield Request(url=url, callback=self.parse)

    def parse(self, response):
        if response.url in self.visited_urls:
            return

        self.visited_urls.add(response.url)

        html_content = response.text
        header_text = response.css('div::text').get()  # Extract header text, adjust as needed

        # Create an item instance and populate it
        item = HtmlContentItem()
        item['url'] = response.url
        item['header'] = header_text.strip() if header_text else 'No Header'
        item['body'] = html_content

        yield item

        hyperlinks = response.css('a::attr(href)').getall()
        for link in hyperlinks:
            link = response.urljoin(link)
            if link.startswith('http') and 'constellationenergy.com' in link and link not in self.visited_urls:
                yield Request(url=link, callback=self.parse_subpage)

    def parse_subpage(self, response):
        if response.url in self.visited_urls:
            return

        self.visited_urls.add(response.url)

        html_content = response.text
        header_text = response.css('div::text').get()  # Extract header text, adjust as needed

        item = HtmlContentItem()
        item['url'] = response.url
        item['header'] = header_text.strip() if header_text else 'No Header'
        item['body'] = html_content

        yield item

        hyperlinks = response.css('a::attr(href)').getall()
        for link in hyperlinks:
            link = response.urljoin(link)
            if link.startswith('http') and 'constellationenergy.com' in link and link not in self.visited_urls:
                yield Request(url=link, callback=self.parse_subpage)

    def closed(self, reason):
        end_time = time.time()
        total_time = end_time - self.start_time
        self.log(f'Total scraping time: {total_time:.2f} seconds')
