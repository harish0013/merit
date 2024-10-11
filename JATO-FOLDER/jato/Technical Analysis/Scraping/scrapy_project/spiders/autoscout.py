import scrapy
import json
import re
from scrapy_project.items import VehicleItem

class VehicleDetailsSpider(scrapy.Spider):
    name = "JATO_autoscout"
    start_url = 'https://www.autoscout24.de/lst?atype=C&cy=D&damaged_listing=exclude&desc=0&hasleasing=true&ocs_listing=include&offer=N&page=1&powertype=kw&search_id=2ayclr8z17x'

    custom_settings = {
        'ROBOTSTXT_OBEY' : False
    }

    def start_requests(self):
        """Initiates the scraping by requesting the first page."""
        yield scrapy.Request(url=self.start_url, callback=self.pagination)

    def pagination(self, response):
        """Handles pagination to request all pages."""
        try:
            # Extract total pages from pagination elements
            total_pages = response.css('li.pagination-item button.FilteredListPagination_button__vFHL3::text').getall()
            last_page = int(total_pages[len(total_pages) - 1])  # Get the last page number

            # Loop through all the pages and send a request for each one
            for page in range(1, last_page + 1):
                pagination_url = f'https://www.autoscout24.de/lst?atype=C&cy=D&damaged_listing=exclude&desc=0&hasleasing=true&ocs_listing=include&offer=N&page={page}&powertype=kw&search_id=v0f99jz8iy&sort=standard&source=listpage_pagination&ustate=N%2CU'
                yield scrapy.Request(url=pagination_url, callback=self.parse)
                break ## testing
        except Exception as e:
            self.logger.error(f"Error in pagination: {e}")

    def parse(self, response):
        """Parses vehicle listings from each page and extracts data."""
        try:
            # Extract JSON data embedded in the script tag
            script_content = response.xpath('//script[@id="__NEXT_DATA__"]/text()').get()

            if script_content:
                json_data = json.loads(script_content)  # Parse the JSON data
                page_props = json_data['props']['pageProps']

                # Ensure page_props is a dictionary
                if isinstance(page_props, list):
                    page_props = page_props[0]

                listings = page_props.get('listings', [])

                # Create an instance of VehicleItem for each listing
                item = response.meta.get('item', VehicleItem())

                for listing in listings:
                    # Extract and assign vehicle details
                    item['Make'] = listing['vehicle'].get('make', 'Not Available')
                    item['Model'] = listing['vehicle'].get('model', 'Not Available')
                    item['Trim'] = listing['vehicle'].get('modelVersionInput', 'Not Available')
                    item['Power_Train'] = listing['vehicleDetails'][3]['data'] if len(
                        listing['vehicleDetails']) > 3 else 'Not Available'

                    # Construct derivative and version names
                    transmission = listing['vehicleDetails'][1]['data']
                    item['Derivative'] = f"{listing['vehicle'].get('modelVersionInput', 'Not Available')} {transmission}"
                    item['Derivative_Translated_English'] = item['Derivative']
                    item['Version_Name'] = f"{item['Make']}{item['Model']}{item['Trim']}{item['Derivative']}{item['Power_Train']}"
                    item['Version_Name_Translated_English'] = item['Version_Name']

                    # Extract additional details about the listing
                    item['Currency'] = 'EURO'
                    item['Delivery_Costs_Retail'] = listing['leasing']['bestOffer'].get('downPayment', '0')
                    item['Country'] = listing['location'].get('countryCode', 'Not Available')
                    item['Research_Date'] = "07.08.2023"
                    item['Customer_Type'] = listing['leasing']['bestOffer'].get('targetGroup', 'Not Available')
                    item['Product_Name'] = listing['vehicle'].get('offerType', 'Not Available')
                    item['Data_Source'] = "Market"
                    item['Other_Sources'] = "Market"
                    item['Vehicle_Price_Reference'] = 'MSRP'

                    # Extract leasing details
                    contract_duration = int(
                        listing['leasing']['bestOffer'].get('duration', 'Not Available').replace(' Monate', ''))
                    item['Of_Monthly_Instalments'] = contract_duration
                    yearly_mileage = int(
                        listing['leasing']['bestOffer'].get('includedMileage', '0').replace(' km', '').replace('.', ''))
                    item['Yearly_Mileage_Km'] = yearly_mileage
                    item['Yearly_Mileage_Miles'] = yearly_mileage * 0.621371
                    item['Total_Contract_Mileage_Km'] = yearly_mileage * (contract_duration / 12)
                    item['Total_Contract_Mileage_Miles'] = (yearly_mileage * 0.621371) * (contract_duration / 12)
                    item['Deposit_Retail'] = listing['leasing']['bestOffer'].get('downPayment', '0')

                    # Distinguish between Business and non-Business customers for instalment amounts
                    if item['Customer_Type'] == 'Business':
                        item['Regular_Monthly_Instalment_Amount_Retail'] = listing['leasing']['bestOffer']['monthlyRateGross']
                        item['Downpayment_Allowance_Base'] = listing['tracking'].get('price', 0)
                    else:
                        item['Downpayment_Allowance_Base'] = listing['tracking'].get('price', 0)
                        item['Regular_Monthly_Instalment_Amount_Base'] = listing['leasing']['bestOffer'][
                            'monthlyRateGross']

                    # Construct the listing URL
                    listing_url = listing.get('url', '')
                    url = f'https://www.autoscout24.de{listing_url}' if listing_url else 'Not Available'
                    item['Web_Source_Url'] = url

                    # Send a request to fetch additional data for this vehicle
                    yield scrapy.Request(url=url, callback=self.data_parse, meta={'item': item})
        except Exception as e:
            self.logger.error(f"Error in parse: {e}")

    def data_parse(self, response):
        """Fetches detailed data about the vehicle from individual listings."""
        try:
            # Extract JSON data from script tag
            script_content = response.xpath('//script[@id="__NEXT_DATA__"]/text()').get()

            if script_content:
                item = response.meta.get('item', VehicleItem())
                json_data = json.loads(script_content)

                data = json_data['props']['pageProps']['listingDetails']

                # Extract additional vehicle data
                item['Number_Of_Doors'] = data['vehicle']['numberOfDoors']
                item['Body_Type'] = data['vehicle']['bodyType']
                item['Product_Description'] = data['vehicle']['paintType']
                item['Built_Option_Pack'] = data['vehicle']['paintType']
                item['Monthly_Payment_Provider_Name'] = response.css('div.LeasingSection_loanBrokerageContainer__iz04Y p::text').get().strip()
                item['Price'] = data['leasingDetails']['bestOffer'].get('finalInstalment','Not Available')
                item['Insurance'] = \
                data['financingAndInsurance']['buttonWithInsurance'][0]['overlay']['fullyComprehensive']['formatted']
                item['Advertised_Price_Point_Monthly_Payment'] = data['vehicle']['offerType']
                item['Insurance_Description'] = 'fully Comprehensive Insurance'

                # Yield the final item
                yield item
        except Exception as e:
            self.logger.error(f"Error in data_parse: {e}")
