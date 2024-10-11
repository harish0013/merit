import scrapy
from scrapy_project.items import VehicleItem
import json
import re


class MobileSpider(scrapy.Spider):
    name = 'JATO_mobile_de'
    allowed_domains = ['suchen.mobile.de']
    start_urls = ['https://suchen.mobile.de/']

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
    }

    cookies = {
        '_bb_lat_long': 'MTIuOTM2OTgwM3w4MC4xNzQwMjAy'
    }

    def start_requests(self):
        # Start by requesting the initial URL to get to the search results page
        yield scrapy.Request(self.start_urls[0], headers=self.headers, cookies=self.cookies, callback=self.pagination)

    def pagination(self, response):
        # Navigate to the search results page directly for simplicity
        # pages_info = response.xpath("div[data-testid='srp-pagination'] > ul > li").getall()
        pages = 50
        for page in range(0,int(pages)+1):
            search_url = f'https://suchen.mobile.de/fahrzeuge/search.html?isSearchRequest=true&lst=p&od=down&pageNumber={page}&ref=srpNextPage&refId=ce2e4d33-a6e6-0d97-4e3c-d1d12e6dc196&s=Car&sb=doc&vc=Car'
            yield scrapy.Request(search_url, headers=self.headers, cookies=self.cookies, callback=self.parse)
            break # testing 

    def process_item(self, val, response):

        item = response.meta.get('item', VehicleItem())
        try:
            item['Make'] = val['make']
            item['Model'] = val['model']
            item['Derivative'] = val['title']
            item['Derivative_Translated_English'] = val['title']
            item['Number_Of_Doors'] = val['attr']['door']
            item['Body_Type'] = val['category']
            item['Power_Train'] = val['attr']['ft']
            item['Version_Name'] = val['make'] + val['model'] + val['title'] + val['attr']['door'] + val['category'] + val['attr']['ft']
            item['Version_Name_Translated_English'] = val['make'] + val['model'] + val['title'] + val['attr']['door'] + val['category'] + val['attr']['ft']
            item['Currency'] = val['price']['grossCurrency']
            item['Price'] = val['price']['gross']
            item['Delivery_Costs_Retail'] = 'Keine Angabe'
            item['Country'] = val['contactInfo']['country']
            item['Research_Date'] = '11.08.2024'
            item['Customer_Type'] = val['leasingRate']['type']
            item['Monthly_Payment_Type'] = 'BALLOON'
            item['Product_Name'] = val['contactInfo']['name']
            item['Monthly_Payment_Provider_Name'] = 'Santander Carcredit'
            item['Monthly_Payment_Provider_Type'] = 'Check24 GmbH'
            item['Interest_Rate_Apr'] = '5,99%'
            item['Interest_Rate_Nominal'] = '5,83%'
            item['Contract_Duration_Months'] = val['leasingRate']['termOfContract']
            item['Yearly_Mileage_Km'] = f"{val['leasingRate']['annualMileage']:,}"
            # item['Yearly Mileage (Miles)': f"{val['leasingRate']['annualMileage'] * 0.621371:,}"
            # item['Total Contract Mileage (Km)': f"{val['leasingRate']['annualMileage'] * (item['leasingRate']['termOfContract'] / 12):,.2f}"
            # item['Total Contract Mileage (Miles)': f"{val['leasingRate']['annualMileage'] * (item['leasingRate']['termOfContract'] / 12) * 0.621371:,.2f}"
            item['Deposit_Retail'] = val['leasingRate']['downPayment']
            # item['Deposit (% Of Price)': f"{(float(item['leasingRate']['downPayment']) / float(item['price']['gross'].replace('€', '').replace('.', '').replace(',', '.').strip())) * 100:,.2f}"
            item['Of_Monthly_Instalments'] = val['leasingRate']['termOfContract']
            item['Regular_Monthly_Instalment_Amount_Retail'] = val['leasingRate']['grossRate']
            item['Additional_Fees_Retail'] = val['leasingRate']['downPayment']
            item['Data_Source'] = 'Market'
            item['Web_Source_Url'] = 'https://suchen.mobile.de/' + val['relativeUrl']
            item['Other_Sources'] = 'Market'
            item['Vehicle_Price_Reference'] = val['price']['netAmount']
            item['Insurance'] = 'Check24 GmbH'
            item['Insurance_Description'] = "CHECK24's car insurance comparison is the only one in Germany to have achieved more than 15 test victories, most recently in the study 'Car insurance comparison portals' (€uro am Sonntag, issue 01/22)."
            item['Reimbursement_Mileage_Retail'] = response.css('dd.nI7AA span::text').get(default='Not Available').strip()

            yield item
        except:
            pass


    def parse(self, response):
        
        # Properly format the string into a JSON object
        data = response.css('body.body script::text').get()
        if data:
            data = data.replace("window.__INITIAL_STATE__ = ", '"key1":')
            data = data.replace("window.__PUBLIC_CONFIG__ = ", ',"key2":')
            data = "{" + data + "}"
            # Now try to load the JSON
            data = json.loads(data)
            page_props = data['key1']['search']['srp']['data']['searchResults']['items']
            

            i = 0
            for val in page_props:
                if val['type'] in ['topAd', 'ad']:
                    yield from self.process_item(val, response)
                    i += 1
                elif val['type'] == 'page1Ads':
                    for sub_data in val['items']:
                        yield from self.process_item(sub_data, response)
                else:
                    i += 1
                    continue