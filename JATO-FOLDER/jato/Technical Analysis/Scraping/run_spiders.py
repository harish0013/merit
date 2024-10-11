from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
import logging

def run_spiders(spiders,parallel=True):

    if parallel:
        process = CrawlerProcess(get_project_settings())
        for spider in spiders:
            logging.info(f"Executing spider crawler {spider}")
            process.crawl(spider)
            logging.info(f"Executing completed for spider crawler {spider}")
        process.start()

    else:
        for spider in spiders:
            process = CrawlerProcess(get_project_settings())
            process.crawl(spider)
            process.start()