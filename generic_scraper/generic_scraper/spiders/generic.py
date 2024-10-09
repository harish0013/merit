import scrapy
from urllib.parse import urlparse
import requests  # To fetch URLs dynamically


class DynamicURLSpider(scrapy.Spider):
    name = "generic_scraper"

    # Define a fallback mechanism to fetch URLs if no valid URL is provided
    def __init__(self, start_url=None, *args, **kwargs):
        super(DynamicURLSpider, self).__init__(*args, **kwargs)

        if start_url and self.is_valid_url(start_url):
            self.start_urls = [start_url]
        else:
            # Dynamically fetch valid URL (example: from an API or hardcoded list)
            self.start_urls = [self.fetch_default_url()]

    def fetch_default_url(self):
        """Function to fetch a default URL dynamically in case the provided start URL is invalid"""
        try:
            # Example: Fetch from an external API, or use a predefined list of URLs
            response = requests.get("https://www.constellationenergy.com/")
            if response.status_code == 200:
                url = response.json().get("url")
                if self.is_valid_url(url):
                    return url
        except Exception as e:
            self.log(f"Error fetching default URL: {e}")

        # Fallback URL if API fails
        return "https://www.constellationenergy.com/"

    def is_valid_url(self, url):
        """Helper function to check if a URL is valid and can be crawled"""
        parsed_url = urlparse(url)
        if parsed_url.scheme in ['http', 'https'] and parsed_url.netloc:
            return True
        return False

    def parse(self, response):
        """Parse the page content and extract links"""
        page_html = response.body.decode('utf-8')
        page_title = response.css('title::text').get()

        # Log the page title
        self.log(f"Scraped page title: {page_title}")

        # Save page content
        filename = f"scraped_content_{urlparse(response.url).netloc}.json"
        with open(filename, 'w') as f:
            f.write(str({
                'url': response.url,
                'title': page_title,
                'html': page_html
            }))

        # Extract and validate all links
        for next_page in response.css('a::attr(href)').getall():
            next_page = response.urljoin(next_page)
            if self.is_valid_url(next_page):
                yield scrapy.Request(next_page, callback=self.parse)
            else:
                self.log(f"Skipping invalid URL: {next_page}")
