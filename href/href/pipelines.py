# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import os
from urllib.parse import urlparse

class SaveHTMLPipeline:
    def process_item(self, item, spider):
        # Extract the header text and URL to create a directory structure
        header = item['header'].replace(' ', '_').replace('/', '_')
        parsed_url = urlparse(item['url'])
        domain = parsed_url.netloc

        # Create a folder structure based on the header and URL path
        folder_path = f"{domain}/{header}/" + parsed_url.path.strip('/').replace('/', '_')
        os.makedirs(folder_path, exist_ok=True)

        # Create a filename for the HTML dump
        file_name = os.path.join(folder_path, 'page.html')

        # Save the HTML content to a file
        with open(file_name, 'w', encoding='utf-8') as f:
            f.write(item['body'])

        return item

