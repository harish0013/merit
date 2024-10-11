# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import re
import pandas as pd
import logging
from azure.storage.blob import BlobServiceClient
import json

class ScrapyProjectPipeline:

    def __init__(self):
        self.items = {}
        self.blob_service_client = BlobServiceClient.from_connection_string("DefaultEndpointsProtocol=https;AccountName=jatoproject;AccountKey=Ih93978inR59FMdrMgZk1kHCNFwpMFQkZrbYYfVIujHG7lIjkwB/ysLJgldgLi2mpd+rzOz6W8dX+ASt6r0+nA==;EndpointSuffix=core.windows.net")
        self.container_client = self.blob_service_client.get_container_client("rawdata")

    def open_spider(self, spider):
        # Initialize a separate list for each spider
        self.items[spider.name] = []

    def close_spider(self, spider):
        try:
            # Convert the list of items to a JSON string
            json_data = json.dumps(self.items.get(spider.name, []), ensure_ascii=False, indent=4)
            
            # Create a unique file name per spider
            file_name = f'{spider.name}_raw_data.json'
            # # # Write JSON data to the file
            with open(file_name, 'w', encoding='utf-8') as f:
                f.write(json_data)
            
            # Upload JSON data directly to Azure Blob Storage
            # blob_client = self.container_client.get_blob_client(file_name)
            # blob_client.upload_blob(json_data, overwrite=True)
        except Exception as e:
            logging.error(f'Error occurred while processing items for {spider.name}: {e}')
            
    def extract_derivative(self, value):
        if value and len(value.split(' ')) > 3:
            pattern = r'\[.*?\]'
            match = re.search(pattern, value)
            if match:
                return re.sub(pattern, '', value)
            return value
        else:
            return value

    def extract_build_option(self, value):
        if value and len(value.split(' ')) > 3:
            pattern = r'\[(.* ?)\]'
            matches = re.findall(pattern, value)
            str = ""
            for match in matches:
                if match:
                    str += match + ' '
            if str:
                return str
            return str
        else:
            return value

    def extract_doors(self, value):
        if value and type(value) is not int and len(value.split(' ')) > 3:
            pattern = r'(\d)[dD]r'
            match = re.search(pattern, value)
            if match:
                return match.group(1)
            return value
        else:
            return value

    def extract_tyre(self, value):
        if value:
            pattern = r'<li>(.*?)<\/li>'
            result = ""
            matches = re.findall(pattern, value)
            if len(matches) > 0:
                for match in matches:
                    result += match + ','
                return result[0:-1]
            else:
                return value
        return value

    def extract_road(self,value):
        if value:
            pattern = r'<li>(.*?)<\/li>'
            result = ""
            matches = re.search(pattern, value)
            if matches:
                return matches.group(1)
            return value
        return value

    def extract_courtesy_car(self, value):
        if value:
            pattern = r'<li>(.*?)<\/li>'
            result = ""
            matches = re.findall(pattern, value)
            if matches:
                return matches[4]
            return value
        return value

    def extract_repair(self, value):
        if value:
            pattern = r'<li>(.*?)<\/li>'
            result = ""
            matches = re.findall(pattern, value)
            if matches:
                return matches[5] + ',' + matches[8]
            return value
        return value

    def extract_provider_name(self, value):
        if value:
            pattern = r'(.*?)<br>'
            matches = re.findall(pattern, value)
            if matches:
                return matches[2].strip()
            return value
        return value


    def process_item(self, item, spider):

        if 'Derivative' in item:
            item['Derivative'] = self.extract_derivative(item.get('Derivative', ''))
        if 'Derivative_Translated_English' in item:
            item['Derivative_Translated_English'] = self.extract_derivative(item.get('Derivative_Translated_English', ''))
        if 'Built_Option_Pack' in item:
            item['Built_Option_Pack'] = self.extract_build_option(item.get('Built_Option_Pack', ''))
        if 'Number_Of_Doors' in item:
            item['Number_Of_Doors'] = self.extract_doors(item.get('Number_Of_Doors', ''))
        if 'Tyres_Description' in item:
            item['Tyres_Description'] = self.extract_tyre(item.get('Tyres_Description', ''))
        if 'Maintenance_Description' in item:
            item['Maintenance_Description'] = self.extract_tyre(item.get('Maintenance_Description', ''))
        if 'Road_Assistance' in item:
            item['Road_Assistance'] = self.extract_road(item.get('Road_Assistance', ''))
        if 'Road_Assistance_Description' in item:
            item['Road_Assistance_Description'] = self.extract_road(item.get('Road_Assistance_Description', ''))
        if 'Repair' in item:
            item['Repair'] = self.extract_repair(item.get('Repair', ''))
        if 'Repair_Description' in item:
            item['Repair_Description'] = self.extract_repair(item.get('Repair_Description', ''))
        if 'Courtesy_Car' in item:
            item['Courtesy_Car'] = self.extract_courtesy_car(item.get('Courtesy_Car', ''))
        if 'Courtesy_Car_Description' in item:
            item['Courtesy_Car_Description'] = self.extract_courtesy_car(item.get('Courtesy_Car_Description', ''))
        if 'Monthly_Payment_Provider_Name' in item:
            item['Monthly_Payment_Provider_Name'] = self.extract_courtesy_car(item.get('Monthly_Payment_Provider_Name', ''))
        # Append item to the list for the specific spider
        if spider.name not in self.items:
            self.items[spider.name] = []
        self.items[spider.name].append(dict(item))
        return item
