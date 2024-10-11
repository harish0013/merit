import scrapy
import json
import re
from scrapy_project.items import VehicleItem


class LeaseScrapSpider(scrapy.Spider):
    name = "JATO_lexautolease"
    allowed_domains = ["quotes.lexautolease.co.uk", "lexautolease.co.uk"]
    start_url = 'https://quotes.lexautolease.co.uk/Quote/GetQuoteManufacturers'

    custom_settings =   {
        'DOWNLOAD_DELAY': 1
        #'AUTOTHROTTLE_ENABLED' : True # adjusts delays dynamically based on server load and request success rate
    }

    cookies = {
        '_cs_c': '0',
        'OPTOUTMULTI': '0:0%7Cc3:0%7Cc5:0%7Cc4:0%7Cc2:0',
        'OPTOUTMULTIMESSAGE': '1',
        's_fid': '442B507E575CEED6-2144776EECBA5F42',
        '_ga': 'GA1.3.1934370789.1723187134',
        '_ga_2K56LZ25NE': 'GS1.3.1724208373.3.1.1724208395.0.0.0',
        'ak_bmsc': '27B591B2CAB8A8862405022363052B36~000000000000000000000000000000~YAAQ2oMsMRmYbpaRAQAAXwAEtBgMRSqQDf6uveDmZv+vbTNuCextaKrEBZtdxj3jzcLGtGHj0erKa4704955qHgcKP26SAQ+LDRXnzwAP4E2A2ziG6EBRrbdAFqPGEG9Ni7X27D1QpIVJUBZrHtsRc0OCI1zkoynYLMUYH0p6gXIGPUor4dtVnrFqnc9yIwcEoaTH47Mtycpn2PAjN8HiXO8Vu9UmbPafAIdQHgt58Qdhn43xXEs1i3JnjK6LtMP7WaZpME5bt/TIYn0iaiZ1jbbZwF+VrfBYuEK4BGw5MghfTc6j+qiwbk/IzWbNAstZsrfZnWQmyuab6W5iBlOKBWLc02JtDTikhiCV6vc8gDEGxIoGc3ckrORqCeyDbeAJ1h6Ub9Kb9XM',
        '_cs_mk_aa': '0.8779684732529942_1725302057582',
        'AMCVS_230D643E5A2550980A495DB6%40AdobeOrg': '1',
        'AMCV_230D643E5A2550980A495DB6%40AdobeOrg': '-1303530583%7CMCMID%7C33943408781722415551482311868790002588%7CMCAAMLH-1725906858%7C12%7CMCAAMB-1725906858%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1725309258s%7CNONE%7CvVersion%7C3.3.0',
        's_cc': 'true',
        'LeasingRoute': 'personal',
        '__RequestVerificationToken': 'PPNEaZ1oFzW3AgXD-4-JNAmIlA3OO69Nh1D2D6jEo8OXn5LTbVs19vk3786lkUqjvyNQu0Ob4Adt4JKYw50_EzQcZ42UNAY4kR4gDmrJm-GXNawWXrLuNck66OOWAnIejE0ZbqlC-aNOsXoT6n06DA2',
        'appSession': 'rd3o00000000000000000000ffff0a1385a5o44302',
        'ASP.NET_SessionId': 'b3wgrx2goy21dc3lhozbaeij',
        'QLA_AuthToken': '630c947a9c804a0881f88b7be7618503',
        's_sq': '%5B%5BB%5D%5D',
        'ADRUM': 's=1725303420888&r=https%3A%2F%2Fwww.lexautolease.co.uk%2Fpersonal-quote-triage%3F0',
        '_cs_id': 'c03784df-f584-a5c2-8ec0-7ce8507f2c2f.1722495230.58.1725303473.1725302057.1719505058.1756659230553.1',
        '_cs_s': '11.5.0.1725305273581',
        'utag_main': 'v_id:01910cb750460026e6d5bda5a3720506f001f0670086e$_sn:44$_se:75$_ss:0$_st:1725305282631$vapi_domain:lexautolease.co.uk$ses_id:1725302057558%3Bexp-session$_pn:11%3Bexp-session',
        'bm_sv': 'A02AFF696076298432AA2C8991B26B60~YAAQ2oMsMZ/IbpaRAQAAwO0ZtBjotvgIv0cY39tUsbs3A2NWjdPgKINhohYdUgJd2ymfe1wT8FeBgpXdMriPqXIK5EzC48/vUOSFzjZvs9E51aYlXYROFkixbl4pdC8onlK1zvrKMHh19+qf1GXJNG2eODpvKOXLadwdcnNPCai7s0nI8SdupF3MnQ49qC9TSP/CowZwgcMCQf06dE6pZu+CFIj8LFm02Z5yx1c1uPtJZdtSR12cazWTyRhVU/vpyUeLuMy5oHvW~1',
    }

    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Language': 'en-US,en;q=0.9,ta;q=0.8,ml;q=0.7',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Content-Type': 'application/json',
        # 'Cookie': '_cs_c=0; OPTOUTMULTI=0:0%7Cc3:0%7Cc5:0%7Cc4:0%7Cc2:0; OPTOUTMULTIMESSAGE=1; s_fid=442B507E575CEED6-2144776EECBA5F42; _ga=GA1.3.1934370789.1723187134; _ga_2K56LZ25NE=GS1.3.1724208373.3.1.1724208395.0.0.0; ak_bmsc=27B591B2CAB8A8862405022363052B36~000000000000000000000000000000~YAAQ2oMsMRmYbpaRAQAAXwAEtBgMRSqQDf6uveDmZv+vbTNuCextaKrEBZtdxj3jzcLGtGHj0erKa4704955qHgcKP26SAQ+LDRXnzwAP4E2A2ziG6EBRrbdAFqPGEG9Ni7X27D1QpIVJUBZrHtsRc0OCI1zkoynYLMUYH0p6gXIGPUor4dtVnrFqnc9yIwcEoaTH47Mtycpn2PAjN8HiXO8Vu9UmbPafAIdQHgt58Qdhn43xXEs1i3JnjK6LtMP7WaZpME5bt/TIYn0iaiZ1jbbZwF+VrfBYuEK4BGw5MghfTc6j+qiwbk/IzWbNAstZsrfZnWQmyuab6W5iBlOKBWLc02JtDTikhiCV6vc8gDEGxIoGc3ckrORqCeyDbeAJ1h6Ub9Kb9XM; _cs_mk_aa=0.8779684732529942_1725302057582; AMCVS_230D643E5A2550980A495DB6%40AdobeOrg=1; AMCV_230D643E5A2550980A495DB6%40AdobeOrg=-1303530583%7CMCMID%7C33943408781722415551482311868790002588%7CMCAAMLH-1725906858%7C12%7CMCAAMB-1725906858%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1725309258s%7CNONE%7CvVersion%7C3.3.0; s_cc=true; LeasingRoute=personal; __RequestVerificationToken=PPNEaZ1oFzW3AgXD-4-JNAmIlA3OO69Nh1D2D6jEo8OXn5LTbVs19vk3786lkUqjvyNQu0Ob4Adt4JKYw50_EzQcZ42UNAY4kR4gDmrJm-GXNawWXrLuNck66OOWAnIejE0ZbqlC-aNOsXoT6n06DA2; appSession=rd3o00000000000000000000ffff0a1385a5o44302; ASP.NET_SessionId=b3wgrx2goy21dc3lhozbaeij; QLA_AuthToken=630c947a9c804a0881f88b7be7618503; s_sq=%5B%5BB%5D%5D; ADRUM=s=1725303420888&r=https%3A%2F%2Fwww.lexautolease.co.uk%2Fpersonal-quote-triage%3F0; _cs_id=c03784df-f584-a5c2-8ec0-7ce8507f2c2f.1722495230.58.1725303473.1725302057.1719505058.1756659230553.1; _cs_s=11.5.0.1725305273581; utag_main=v_id:01910cb750460026e6d5bda5a3720506f001f0670086e$_sn:44$_se:75$_ss:0$_st:1725305282631$vapi_domain:lexautolease.co.uk$ses_id:1725302057558%3Bexp-session$_pn:11%3Bexp-session; bm_sv=A02AFF696076298432AA2C8991B26B60~YAAQ2oMsMZ/IbpaRAQAAwO0ZtBjotvgIv0cY39tUsbs3A2NWjdPgKINhohYdUgJd2ymfe1wT8FeBgpXdMriPqXIK5EzC48/vUOSFzjZvs9E51aYlXYROFkixbl4pdC8onlK1zvrKMHh19+qf1GXJNG2eODpvKOXLadwdcnNPCai7s0nI8SdupF3MnQ49qC9TSP/CowZwgcMCQf06dE6pZu+CFIj8LFm02Z5yx1c1uPtJZdtSR12cazWTyRhVU/vpyUeLuMy5oHvW~1',
        'Origin': 'https://quotes.lexautolease.co.uk',
        'Pragma': 'no-cache',
        'Referer': 'https://quotes.lexautolease.co.uk/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
        '__RequestVerificationToken': 'f-IJSkkhxftkuwAcwDI8Ftt6kZWB_-bKcejVK1WKrxbyW6mCSMWCLtNkZwZSHuKPsyRfTLqsMWC89_ygxRYeYTMj51X-h7B_6c2RruGnXWBr-N2QTCNbBi7NQ4xh83_p5SKnrzxCxBSQBjIDMITQ9kDmkjlbndk-suDiGS_OPwY1',
        'sec-ch-ua': '"Chromium";v="128", "Not;A=Brand";v="24", "Google Chrome";v="128"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }

    def start_requests(self):
        """Starts the initial request for both personal and business customers."""
        customer_type = ['personal', 'business']

        for customer in customer_type:
            manufacturer_payload = {
                'busType': customer,
                'defaultType': None,
                'vechicleType': 'ALL',
            }

            try:
                # Sending POST request to get manufacturer data
                yield scrapy.Request(
                    url=self.start_url,
                    method='POST',
                    body=json.dumps(manufacturer_payload),
                    headers=self.headers,
                    cookies=self.cookies,
                    meta={'customer': customer},
                    callback=self.manufacturer_parse
                )
            except Exception as e:
                self.logger.error(f"Error in start_requests: {e}")
            # break  # Breaking for testing purposes

    def contract_termination(self, response):
        """Parses the contract termination details."""
        item = response.meta.get('item', VehicleItem())

        try:
            cost_to_terminate_contract_description = response.xpath(
                '/html/body/div[1]/div/div/div[2]/div/div/div[1]/div[2]/div/div/div[2]/div/div/div/div/div[11]/div[2]/div/div/div/div[2]/div/div/div/div/div[2]/table/tbody/tr[4]/td[2]/p/big/text()').get()
            # Extracting cost to terminate contract
            item['Cost_To_Terminate_Contract_Description'] = re.search(r'\d.*?\.',
                                                                       cost_to_terminate_contract_description).group(
                0) if re.search(r'\d.*?\.', cost_to_terminate_contract_description) else None
        except Exception as e:
            self.logger.error(f"Error in contract_termination: {e}")
            item['cost_to_terminate_contract_description'] = None

        yield item

    def service_and_maintenance_parse(self, response):
        """Parses the service and maintenance data."""
        item = response.meta.get('item', VehicleItem())

        try:
            # Extracting various fields from service and maintenance section
            service_and_maintenance = \
            response.css('div#divImportantSection div p::text').getall()[2].strip().split('.')[0]
            item['Maintenance_Description'] = service_and_maintenance
            item['Repair'] = service_and_maintenance
            item['Repair_Description'] = service_and_maintenance
            item['Service'] = service_and_maintenance
            item['Service_Description'] = service_and_maintenance
            item['Tyres'] = service_and_maintenance
            item['Tyres_Description'] = service_and_maintenance
            item['Flexible_Early_Cancellation_Possible'] = 'Y'

            # Extracting monthly payment provider details
            payment_provider = response.css('div#divImportantSection div p::text').getall()[1].strip()
            item['Monthly_Payment_Provider_Name'] = re.search(r'.*?\)', payment_provider).group(0) if re.search(r'.*?\)',payment_provider) else None
            item['Monthly_Payment_Provider_Type'] = f"{payment_provider.split(' ')[0]} {payment_provider.split(' ')[1]}"
        except Exception as e:
            self.logger.error(f"Error in service_and_maintenance_parse: {e}")

        # Sending request for road assistance details
        road_assistance_url = 'https://www.lexautolease.co.uk/personal/maintenance/breakdown-assistance'
        yield scrapy.Request(
            url=road_assistance_url,
            headers=self.headers,
            cookies=self.cookies,
            meta={'item_type': 'assistance', 'item': item},
            callback=self.road_assistance_parse
        )

    def road_assistance_parse(self, response):
        """Parses the road assistance information."""
        item = response.meta.get('item', VehicleItem())

        try:
            road_assistance = response.css('div.content-bulltd-description p::text').getall()
            item['Road_Assistance'] = re.search(r'-\d,.*', road_assistance[0].strip()).group(0) if re.search(r'-\d,.*',
                                                                                                             road_assistance[
                                                                                                                 0].strip()) else None
            item['Road_Assistance_Description'] = road_assistance[1].strip()
        except Exception as e:
            self.logger.error(f"Error in road_assistance_parse: {e}")

        # Sending request for contract termination details
        contract_url = 'https://www.lexautolease.co.uk/business/smaller-business-faq/end-of-contract'
        yield scrapy.Request(
            url=contract_url,
            headers=self.headers,
            cookies=self.cookies,
            meta={'item_type': 'contract', 'item': item},
            callback=self.contract_termination
        )

    def manufacturer_parse(self, response):
        """Parses the manufacturer data."""
        try:
            manufacturer_data = json.loads(response.text)
        except json.JSONDecodeError as e:
            self.logger.error(f"Error decoding manufacturer JSON: {e}")
            return

        model_url = 'https://quotes.lexautolease.co.uk/Quote/GetQuoteModels'

        flag = True
        for id in manufacturer_data:
            if flag:
                flag = False
                continue
            # Sending request to get models for the manufacturer
            model_payload = {
                "busType": response.meta['customer'],
                "manufacturerID": id['Manufacturer_ID'],
                "defaultType": None,
                "vechicleType": "ALL"
            }
            try:
                yield scrapy.Request(
                    url=model_url,
                    method='POST',
                    body=json.dumps(model_payload),
                    headers=self.headers,
                    cookies=self.cookies,
                    meta={'customer': response.meta['customer']},
                    callback=self.model_parse
                )
            except Exception as e:
                self.logger.error(f"Error in manufacturer_parse: {e}")
            break  # Breaking for testing purposes

    def model_parse(self, response):
        """Parses the model data."""
        try:
            model_data = json.loads(response.text)
        except json.JSONDecodeError as e:
            self.logger.error(f"Error decoding model JSON: {e}")
            return

        varient_url = 'https://quotes.lexautolease.co.uk/Quote/GetQuoteVariants'

        for id in model_data:
            varient_payload = {
                "busType": response.meta['customer'],
                "manufacturerID": id['Manufacturer_ID'],
                "modelId": id['Model_Id'],
                "defaultType": None,
                "vechicleType": "ALL"
            }
            try:
                # Sending request to get variant data
                yield scrapy.Request(
                    url=varient_url,
                    method='POST',
                    body=json.dumps(varient_payload),
                    headers=self.headers,
                    cookies=self.cookies,
                    meta={'customer': response.meta['customer']},
                    callback=self.varient_parse
                )
            except Exception as e:
                self.logger.error(f"Error in model_parse: {e}")
            break  # Breaking for testing purposes

    def varient_parse(self, response):
        """Parses the variant data."""
        try:
            varient_data = json.loads(response.text)
        except json.JSONDecodeError as e:
            self.logger.error(f"Error decoding variant JSON: {e}")
            return

        search_url = 'https://quotes.lexautolease.co.uk/Quote/Search'

        for id in varient_data:
            search_payload = {
                "BusinessType": response.meta['customer'],
                "vechicleType": "ALL",
                "Commercial": 0,
                "manufacturerID": id['Manufacturer_ID'],
                "modelId": id['Model_Id'],
                "VariantId": id['Variant_Id'],
                "BodyStyles": None,
                "FuelTypes": None,
                "Co2Band": "",
                "MileagePerAnnum": "10000",
                "ContractDuration": "48",
                "Transmission": None,
                "NumberOfDoors": None,
                "Maintenance": "0",
                "FleetSize": 1,
                "Limit": 12,
                "Offset": 1,
                "Ordering": "low",
                "RdeType": "",
                "AffinityCode": "0"
            }
            try:
                yield scrapy.Request(
                    url=search_url,
                    method='POST',
                    body=json.dumps(search_payload),
                    headers=self.headers,
                    cookies=self.cookies,
                    meta={'customer': response.meta['customer']},
                    callback=self.search_parse
                )
            except Exception as e:
                self.logger.error(f"Error in varient_parse: {e}")
            break  # Breaking for testing purposes

    def search_parse(self, response):
        """Parses the search data for vehicle quotes."""
        try:
            search_data = json.loads(response.text)
        except json.JSONDecodeError as e:
            self.logger.error(f"Error decoding search JSON: {e}")
            return

        encryptedURL = search_data['vehicles'][0]['encryptedQuoteParameters']
        ContractTypeId = search_data['vehicles'][0]['ContractTypeId']
        product_url = f'https://quotes.lexautolease.co.uk/quotes/details/personal/1/{encryptedURL}/0/False'

        # Yield for car and financial data



        quote_url = 'https://quotes.lexautolease.co.uk/Quote/UpdateQuote'

        mileage_lst = [5000, 8000, 10000, 15000, 20000, 25000, 30000, 35000, 40000, 45000, 50000]
        contract_lst = [24, 36, 48, 60]
        maintenance_lst = [0, 1]
        initial_rent = [7, 23, 26, 43, 27]  # values for months (1,3,6,9,12)

        for contract in contract_lst:
            for mileage in mileage_lst:
                for maintenance in maintenance_lst:
                    for rent in initial_rent:
                        quote_payload = {
                            'fleetSize': 1,
                            'contractType': 'personal',
                            'contractTypeId': ContractTypeId,
                            'mileage': mileage,
                            'term': contract,
                            'paymentPlanId': rent,
                            'maintenance': maintenance,
                            'selectedOptions': '',
                            'affinityCode': '0',
                            'encryptedURL': encryptedURL,
                        }
                        try:
                            yield scrapy.Request(
                                url=quote_url,
                                method='POST',
                                body=json.dumps(quote_payload),
                                headers=self.headers,
                                cookies=self.cookies,
                                callback=self.quote_parse,
                                meta={'maintenance': maintenance, 'customer': response.meta['customer'],
                                      'url': product_url, 'item_type': 'product'}
                            )
                        except Exception as e:
                            self.logger.error(f"Error in search_parse: {e}")
                        break  # Breaking for testing purposes
                    break ## Testing purpose
                break ## Testing purpose
            break ## Testing purpose

    def quote_parse(self, response):
        """Parses the detailed vehicle quote data."""
        if response.status != 200:
            self.logger.info(f'Request Failed, Working on next Request')
            return

        item = response.meta.get('item', VehicleItem())

        try:
            data = json.loads(response.text)

            # Car Specifications
            item['Make'] = data['Vehicle']['Manufacturer']
            item['Model'] = data['Vehicle']['Model']
            item['Body_Type'] = data['Vehicle']['Variant'].split(' ')[1]
            item['Trim'] = data['Vehicle']['Variant']
            item['Number_Of_Doors'] = data['Vehicle']['Variant']
            item['Built_Option_Pack'] = data['Vehicle']['Variant']
            item['Derivative'] = data['Vehicle']['Variant']
            item['Derivative_Translated_English'] = data['Vehicle']['Variant']
            item['Configurator_Model_Year'] = data['Vehicle']['ModelYear']
            item['Version_Name'] = f"{data['Vehicle']['Manufacturer']} {data['Vehicle']['Variant']}"
            item['Version_Name_Translated_English'] = f"{data['Vehicle']['Manufacturer']} {data['Vehicle']['Variant']}"
            item['Flexible_Early_Cancellation_Possible'] = 'Y'

            # Other Information
            item['Currency'] = 'EURO'
            item['Country'] = 'Germany'
            item['Data_Source'] = 'Market'
            item['Other_Sources'] = 'Market'
            item['Web_Source_Url'] = f"https://quotes.lexautolease.co.uk/quotes/details/personal/1/{data['encryptedQuoteParameters']}/0/False"

            # Leasing Information
            initial_rent = {7: 1, 23: 3, 26: 6, 43: 9, 27: 12}
            item['Contract_Duration_Months'] = data['Vehicle']['Term']
            item['Of_Monthly_Instalments'] = int(data['Vehicle']['Term']) - 1
            item['Of_Monthly_Payments_In_Advance'] = initial_rent.get(data['Vehicle']['PaymentPlanId'])
            item['Maintenance'] = response.meta['maintenance']
            item['Customer_Type'] = response.meta['customer']

            # Separation of Business and Private fields
            if data['Vehicle']['Contract'] == 'personal':
                item['Regular_Monthly_Instalment_Amount_Retail'] = data['Vehicle']['MonthlyRental']
                item['First_Monthly_Instalment_Amount_Retail'] = data['Vehicle']['Initial_Payment']
            else:
                item['Regular_Monthly_Instalment_Amount_Base'] = data['Vehicle']['MonthlyRental']
                item['First_Monthly_Instalment_Amount_Base'] = data['Vehicle']['Initial_Payment']

            item['Yearly_Mileage_Miles'] = data['Vehicle']['Mileage']
            item['Yearly_Mileage_Km'] = data['Vehicle']['Mileage'] * 1.60934
            item['Total_Contract_Mileage_Miles'] = data['Vehicle']['Mileage'] * (data['Vehicle']['Term'] / 12)
            item['Total_Contract_Mileage_Km'] = (data['Vehicle']['Mileage'] * (data['Vehicle']['Term'] / 12)) * 1.60934
        except Exception as e:
            self.logger.error(f"Error in quote_parse: {e}")

        yield item