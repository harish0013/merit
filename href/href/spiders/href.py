import scrapy
from scrapy.http import Request
from urllib.parse import urlparse, urljoin
import time
from href.items import HtmlContentItem  # Import the item class

class EnphaseScraper(scrapy.Spider):
    name = 'href'
    start_urls = ['https://enphase.com/']
net
    visited_urls = set()

    def start_requests(self):
        self.start_time = time.time()
        for url in self.start_urls:
            yield Request(url=url, callback=self.parse)

    def parse(self, response):
        normalized_url = self.normalize_url(response.url)
        if normalized_url in self.visited_urls:
            return

        self.visited_urls.add(normalized_url)

        html_content = response.text
        header_text = response.css('div::text').get()  # Extract header text, adjust as needed

        # Create an item instance and populate it
        item = HtmlContentItem()
        item['url'] = normalized_url
        item['header'] = header_text.strip() if header_text else 'No Header'
        item['body'] = html_content

        yield item

        # Extract and follow links
        hyperlinks = response.css('a::attr(href)').getall()
        for link in hyperlinks:
            full_link = urljoin(response.url, link)  # Create absolute URLs
            normalized_link = self.normalize_url(full_link)
            if normalized_link.startswith('http') and 'enphase.com' in normalized_link and normalized_link not in self.visited_urls:
                yield Request(url=normalized_link, callback=self.parse)

    def normalize_url(self, url):
        # Normalize the URL to avoid visiting the same page multiple times
        parsed_url = urlparse(url)
        return parsed_url.scheme + '://' + parsed_url.netloc + parsed_url.path.rstrip('/')

    def closed(self, reason):
        end_time = time.time()
        total_time = end_time - self.start_time
        self.log(f'Total scraping time: {total_time:.2f} seconds')
