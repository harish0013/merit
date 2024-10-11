from typing import Iterable
import scrapy
from scrapy_project.items import VehicleItem
import json
import re

class LeaseScrapSpider(scrapy.Spider):
    name = "JATO_selectalease"
    allowed_domains = ["www.selectalease.co.uk"]
    url = 'https://www.selectalease.co.uk'

    cookies = {
        'PHPSESSID': 'dquutoqo7tvqsmev2epc43k085',
        'MoneypennyRef': 'https%3A%2F%2Fwww.selectalease.co.uk%2F%20',
        'MoneypennyHistory': '22#',
        'MoneypennyUserAlias': '%23',
        'MoneypennyVisit': '1#1725303202',
    }

    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Language': 'en-US,en;q=0.9,ta;q=0.8,ml;q=0.7',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        # 'Cookie': 'PHPSESSID=dquutoqo7tvqsmev2epc43k085; MoneypennyRef=https%3A%2F%2Fwww.selectalease.co.uk%2F%20; MoneypennyHistory=22#; MoneypennyUserAlias=%23; MoneypennyVisit=1#1725303202',
        'Pragma': 'no-cache',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Chromium";v="128", "Not;A=Brand";v="24", "Google Chrome";v="128"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }


    def start_requests(self):
        """
        Start the scraping process by requesting the main pages for vehicles and services.
        """
        yield scrapy.Request(url=f'{self.url}/vehicle-service-and-maintenance-quote', cookies=self.cookies, headers=self.headers,callback=self.services_and_maintenance,meta={'item_type': 'service'})

    def pagination(self, response):
        """
        Handles pagination on the vehicle listing page. It iterates over the paginated vehicle list.
        """
        try:
            total_results = int(response.css('p.pagnav-text.robonav b::text').get().strip())  # 20 results per page for 3470 results
            cal = 10 - (total_results % 10)
            total = total_results - (20 - cal)
            page = 0
            while True:
                url = f"https://www.selectalease.co.uk/search-cars?offset={page}"
                yield scrapy.Request(url=url, callback=self.parse_url, cookies=self.cookies, headers=self.headers,meta=response.meta)
                page += 10
                if page > total:
                    break
                break ## Testing purpose
        except Exception as e:
            self.logger.error(f"Error in pagination: {e}")

    def extract_financial_data(self, script_content, var_name):
        """
        Extracts data for a given variable pattern from script content.

        Args:
            script_content (str): The content of the script tag.
            var_name (str): The name of the variable to extract.

        Returns:
            list: The extracted data as a Python list.
        """
        try:
            pattern = fr'var {var_name}\s*=\s*(\[.*?\]);'
            match = re.search(pattern, script_content)

            if match:
                var_data_str = match.group(1)
                # Convert the string representation of the list to an actual list
                var_data_list = eval(var_data_str)
                return var_data_list
            else:
                return None
        except Exception as e:
            self.logger.error(f"Error extracting financial data for {var_name}: {e}")
            return None

    def services_and_maintenance(self, response):
        """
        Parses the service and maintenance information from the service page.

        Args:
            response: The HTTP response from the service page.
        """
        try:
            item = response.meta.get('item', VehicleItem())
            service_section = response.css('ul.ul-bullets li::text').getall()

            item['Repair'] = service_section[0]
            item['Repair_Description'] = service_section[0]
            item['Service'] = service_section[0]
            item['Service_Description'] = service_section[0]
            item['Maintenance_Description'] = service_section[0]
            item['Tyres'] = service_section[4]
            item['Tyres_Description'] = service_section[4]
            item['Road_Assistance'] = service_section[3]
            item['Road_Assistance_Description'] = service_section[3]
            item['Courtesy_Car'] = service_section[9]
            item['Courtesy_Car_Description'] = service_section[9]

            # Pass the item with service maintenance data to the next request
            request = scrapy.Request(url=f'{self.url}/search-cars', callback=self.pagination,
                                     meta={'item_type': 'vehicle', 'item': item})
            yield request

        except Exception as e:
            self.logger.error(f"Error parsing service and maintenance data: {e}")

    def parse_url(self, response):
        """
        Parses the URL from the pagination page and calls the parse method for further data extraction.

        Args:
            response: The HTTP response from the pagination page.
        """
        try:

            container_url = response.css('div.listing.calas-table-listing > div::attr(data-url)').getall()
            for product_url in container_url:
                car_list_info_url = self.url + product_url
                yield scrapy.Request(
                    url=car_list_info_url,
                    callback=self.parse,
                    cookies=self.cookies, 
                    headers=self.headers,
                    meta={'product_url': car_list_info_url, **response.meta} # 'item_type': item_type, , 'item': item
                )
                break ## Testing purpose
        except Exception as e:
            self.logger.error(f"Error in parse_url: {e}")

    def parse(self, response):
        """
        Parses vehicle details, financial information, and specifications from the individual vehicle page.

        Args:
            response: The HTTP response from the vehicle details page.
        """
        try:

            item_type = response.meta['item_type'] # holds value 'vehicle' which is passed from service_and_maintenence()
            item = response.meta.get('item', VehicleItem()) # fetches the item containing data of services_and_maintenance()

            # Car basic information (make, model, body type)
            spec_data = response.xpath('/html/body/div[2]/div[3]/div/div/h1/text()').get().strip()
            spec_data_feature = response.css('h2.dealpage-deriv::text').get().strip()

            item['Make'] = spec_data.split(' ')[0]
            item['Model'] = spec_data.split(' ')[1]
            item['Body_Type'] = spec_data.split(' ')[2]
            item['Derivative'] = spec_data_feature
            item['Derivative_Translated_English'] = spec_data_feature
            item['Trim'] = (response.css('div.dealpage-title-extra.display-768px-up::text').get() or 'Not Available').strip().split('|')[1]
            item['Built_Option_Pack'] = spec_data_feature
            number_of_doors = (response.css('div.dealpage-title-extra.display-768px-up::text').get() or 'Not Available').strip().split(' ')[0]
            item['Number_Of_Doors'] = number_of_doors

            # Country and currency information
            item['Currency'] = 'Euro'
            item['Country'] = 'Germany'
            item['Research_Date'] = '01-08-2024'
            item['Data_Source'] = "Market"
            item['Other_Sources'] = "Market"
            item['Web_Source_Url'] = response.meta['product_url']
            item['Published_End_Date'] = json.loads(response.css('div.wi-100pc script::text').getall()[1])['offers']['priceValidUntil']
            item['Flexible_Early_Cancellation_Possible'] = "Y"
            item['Road_Tax'] = 'Y'

            # Leasing Information
            leasing_information = response.css('div.topsection')
            item['Customer_Type'] = (leasing_information.css('div.simput.simform-input-buttons.dealpage-calc.cx2 div.but.on::text').get() or 'Not Available').strip()
            item['Product_Name'] = f"{item['Customer_Type']} Car Lease"
            price = leasing_information.css('div.features div::text').getall()
            item['Price'] = price[len(price)-1]
            item['Delivery_Costs_Retail'] = 0
            item['Advertised_Price_Point_Monthly_Payment'] = 'Yes' if leasing_information.css('div.dealtags::text').get() else 'No'

            # Car specification
            specifications = leasing_information.css('div.features div::text').getall()
            for i in range(0, len(specifications)):
                if i < len(specifications) and specifications[i] == 'Model year':
                    item['Configurator_Model_Year'] = specifications[i + 1]
                    i += 1
                if i < len(specifications) and specifications[i] == 'Fuel type':
                    item['Power_Train'] = specifications[i + 1]
                    i += 1
                if i < len(specifications) and specifications[i] == 'Manufacturer RRP':
                    item['Price'] = specifications[i + 1]
                    item['Vehicle_Price_Reference'] = specifications[i + 1]
                    i += 1

            item['Version_Name'] = f"{spec_data.split(' ')[0]} {spec_data.split(' ')[1]} {spec_data_feature} {number_of_doors}Dr {item['Power_Train']} {spec_data.split(' ')[2]}"
            item['Version_Name_Translated_English'] = f"{spec_data.split(' ')[0]} {spec_data.split(' ')[1]} {spec_data_feature} {number_of_doors}Dr {item['Power_Train']} {spec_data.split(' ')[2]}"

            # Financial Information
            finance_detail_script = response.css('div.wi-100pc script::text').get()
            contract_duration_lst = []
            initial_rent_lst = []
            mileage_lst = []
            maintenance_lst = []

            contract_duration_val = leasing_information.css('div.simput.simform-input-buttons.dealpage-calc.cx4 div.but')
            for val in contract_duration_val:
                contract_duration_lst.append(int(val.css('::text').get().strip()))

            initial_rent_val = response.css('div.selector-initialrental div.but::text').getall()
            for val in initial_rent_val[2:]:
                initial_rent_lst.append(val)

            mileage_val = leasing_information.css('div.simput.simform-input-select.dealpage-calc ul li')
            for val in mileage_val:
                mileage_lst.append(int(val.css('::text').get().strip().split()[0]))

            maintenance_val = leasing_information.css('div.selector-maintenance div.simput.simform-input-buttons.dealpage-calc.cx2 div.but')
            for val in maintenance_val:
                maintenance_lst.append(int(val.css('::attr(data-value)').get()))

            index = 0
            customer_type_lst = leasing_information.css('div.simput.simform-input-buttons.dealpage-calc.cx2 div.but::text').getall()
            for months in initial_rent_lst:
                for service in maintenance_lst:
                    for duration in contract_duration_lst:
                        for mileage in mileage_lst:
                            for customer_type in customer_type_lst:
                                item['Customer_Type'] = (customer_type or 'Not Available').strip()
                                item['Product_Name'] = f"{customer_type} Car Lease" if customer_type else 'Not Availabe'
                                var_name = f"{item['Customer_Type'].lower()[0:1]}_{duration}_{int(mileage / 1000)}_{service}"
                                finance_lst_org = self.extract_financial_data(finance_detail_script, var_name)  # [2:7]
                                if finance_lst_org is None:
                                    continue
                                # Create a new item for each installment
                                new_item = item.copy()
                                finance_lst = finance_lst_org[2:7]
                                new_item['Contract_Duration_Months'] = duration
                                new_item['Of_Monthly_Payments_In_Advance'] = months
                                new_item['Of_Monthly_Instalments'] = int(months) - 1
                                new_item['Yearly_Mileage_Miles'] = mileage
                                # new_item['yearly_mileage_km'] = round(mileage * 1.60934)
                                # new_item['total_contract_mileage_miles'] = round(mileage * (duration / 12))
                                # new_item['total_contract_mileage_km'] = round((mileage * (duration / 12)) * 1.60934)
                                maintenance_amount = leasing_information.css(
                                    'div.selector-maintenance div span::text').get().strip().split(' ')
                                if len(maintenance_amount) > 7:
                                    new_item['Maintenance_Amount'] = maintenance_amount[8][1:]
                                if service == 1:
                                    new_item['Maintenance'] = "Yes"
                                else:
                                    new_item['Maintenance'] = 'No'

                                if customer_type == 'Business':
                                    new_item['Regular_Monthly_Instalment_Amount_Retail'] = finance_lst[index]
                                    new_item['First_Monthly_Instalment_Amount_Retail'] = finance_lst[index] * int(
                                        months)
                                    new_item['Additional_Fees_Retail'] = finance_lst_org[9]
                                else:
                                    new_item['Regular_Monthly_Instalment_Amount_Base'] = finance_lst[index]
                                    new_item['First_Monthly_Instalment_Amount_Base'] = finance_lst[index] * int(months)
                                    new_item['Additional_Fees_Base'] = finance_lst_org[9]

                                yield new_item

        except Exception as e:
            self.logger.error(f"Error in parse: {e}")