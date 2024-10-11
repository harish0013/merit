import scrapy
import unicodedata
from scrapy_project.items import VehicleItem
import json
import re

class SixtLeasingSpider(scrapy.Spider):
    name = 'JATO_sixt_neuwagen'
    allowed_domains = ['sixt-neuwagen.de']
    start_urls = ["https://www.sixt-neuwagen.de/konfigurieren?customerType=private"]

    custom_settings = {
        'RETRY_ENABLED': True,
        'RETRY_TIMES': 5,  # Reduce the number of retries to minimize delays
        'RETRY_HTTP_CODES': [429, 500, 502, 503, 504],
        'DOWNLOAD_DELAY': 0.5,  # Lower the delay to speed up requests
        'AUTOTHROTTLE_ENABLED': True,
        'AUTOTHROTTLE_START_DELAY': 0.5,  # Reduce initial download delay
        'AUTOTHROTTLE_MAX_DELAY': 5,  # Lower the maximum download delay
        'AUTOTHROTTLE_TARGET_CONCURRENCY': 3.0,  # Increase concurrency to send more requests in parallel
        'AUTOTHROTTLE_DEBUG': False  # Disable throttling debug info to speed up logging
    }

    cookies = {
        '__cmpconsent44521': 'CQCqRqQQCqRqQAfVwBDEA_EgAAAAAAAAAAigCkQAwARAAqAKQAAAAAA',
        '__cmpcccu44521': 'aBQCsTXFgBQAzADQAGwCMAAQACAAIAAcABYAFwANAAeABQAEEAQ4AxACFgWYBMSCb0FGgKRwA1n77nmuedhFQA',
        '_gcl_au': '1.1.1372237939.1722503725',
        '_fbp': 'fb.1.1722503729729.526819052739875969',
        'campaign': 'top30',
        'mf_user': '7585c6c6ec6e2adfb32c4830745aecc5|',
        'cf_clearance': 'YtaHqzC2PKZogvxYIn3PqdVaMJMRTulcmn7T9Ugb6qs-1722922425-1.0.1.1-Q6Yj.ps0H0V1ymZpW8R69uG8.dnn2RvBaJl81sh_w9E5U6fZwf8KXuIAj7aO.h3Majai_00iznHTO7oKDQQynA',
        'saleschannel': 'organic',
        'snst': '%7B%22242%22%3A%7B%22splitname%22%3A%22id_now_bonus_flow%22%2C%22splitvariantname%22%3A%22neue+Splitvariante%22%2C%22distribution%22%3A%221%22%2C%22splitvariantid%22%3A242%7D%2C%22243%22%3A%7B%22splitname%22%3A%22id_now_bonus_flow_cookie_access%22%2C%22splitvariantname%22%3A%22neue+Splitvariante%22%2C%22distribution%22%3A%221%22%2C%22splitvariantid%22%3A243%7D%2C%223007%22%3A%7B%22splitname%22%3A%22leila2_startpage%22%2C%22splitvariantname%22%3A%22leila2_startpage_new%22%2C%22distribution%22%3A%2299%22%2C%22splitvariantid%22%3A301%7D%2C%222000%22%3A%7B%22splitname%22%3A%22best_price_logic%22%2C%22splitvariantname%22%3A%22best_price_logic%22%2C%22distribution%22%3A%221%22%2C%22splitvariantid%22%3A2000%7D%2C%223004%22%3A%7B%22splitname%22%3A%22leila2_integration%22%2C%22splitvariantname%22%3A%22release1_leila2%22%2C%22distribution%22%3A%22100%22%2C%22splitvariantid%22%3A447%7D%2C%222222%22%3A%7B%22splitname%22%3A%22wltp_feature%22%2C%22splitvariantname%22%3A%22wltp_feature%22%2C%22distribution%22%3A%221%22%2C%22splitvariantid%22%3A2222%7D%7D',
        '_conv_v': 'vi%3A1*sc%3A1*cs%3A1722503717*fs%3A1722503717*pv%3A1046*exp%3A%7B100479078.%7Bv.1004191852-g.%7B%7D%7D-100479082.%7Bv.1-g.%7B%7D%7D%7D*seg%3A%7B%7D',
        'originalLocation': 'https://www.sixt-neuwagen.de/konfigurieren/audi?customerType=private',
        'sessionCount': '18',
        'LVKD': 'P',
        'gtag_ga': 'GA1.2.2070224118.1723875327',
        '_clck': '1jwxipj%7C2%7Cfoe%7C0%7C1674',
        '_ga': 'GA1.1.59857357.1723882978',
        '_ga_K47KCJ4FFT': 'GS1.1.1723882978.1.0.1723883101.0.0.0',
        'vehicleConfig': '%7B%22vehicleId%22%3A%22822896920240520%22%2C%22vehicleOptions%22%3A%5B%228228969%7C1007%22%2C%228228969%7C1008%22%5D%2C%22contractType%22%3A%22VARIO%22%2C%22term%22%3A48%2C%22mileage%22%3A10000%2C%22initialPayment%22%3A%7B%22type%22%3A%22ABSOLUTE%22%2C%22amount%22%3A%220%22%7D%2C%22serviceProducts%22%3A%5B%22SUNPRO_DAMAGE_MANAGEMENT%22%5D%2C%22delivery%22%3A%7B%22paymentType%22%3A%22ONE_TIME%22%2C%22optionId%22%3A%22DEALER_PICKUP%22%2C%22deliveryType%22%3A%22DEALER_PICKUP%22%7D%2C%22vehicleNameParts%22%3A%5B%22Dacia%22%2C%22Sandero%22%2C%22Schr%C3%A4ghecklimousine%22%5D%2C%22vehicleImageUrl%22%3A%22https%3A%2F%2Fvehicle.static.prod.or.sixt-leasing.com%2FDACIA%2FSANDERO%2F2024%2FHA%2F5%2F123338b713f29826240e5bfb6b610e456c46dfd0.png%22%7D',
        'pageviewCount': '49',
        'dicbo_id': '%7B%22dicbo_fetch%22%3A1723885017050%7D',
        '_clsk': '1ro539m%7C1723885017883%7C15%7C1%7Cz.clarity.ms%2Fcollect',
        '__cf_bm': 'GO7dGGOmLpcLAqO_Qg3Z0Guq4TlyK7TzJ4IIZmUmbB8-1723885023-1.0.1.1-DVdOgRwAoMe50ij9KDxebGhmcdrd6P2yjytaE1RkzMVhfqNiSQpnPAuvkxNHcRMhY_tdpgXGVOdANu0YhYEqUQ',
        'gtag_ga_K47KCJ4FFT': 'GS1.2.1723882893.3.1.1723885032.0.0.0',
        'mf_1b6d36a5-b2b0-47fb-8f39-3b8e72dbd941': '1f4438c85ea639bad45c55944a9fb727|081722813714cfff0b52edd1f80236618eb9aac2.7553023213.1723883062682$081726930a467c4a1ea77d6adf212b7b38185944.2652562946.1723883066495$08172905318498e2df823683f098830a8ec62a74.-603121347.1723883069707$08175086b02915c0dda04521cce1c410507abd1a.-603121347.1723883150389$08170050326fa40a20e41ef45d6bfae92a2256ce.-603121347.1723883280653$0817565939fd4bde3f2e556a6b99fcca62c1b042.47.1723885016164|1723885045961|900359224_-314497661|14||||1|18.10|1.17588',
    }

    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'en-US,en;q=0.9',
        'cache-control': 'no-cache',
        # 'cookie': '__cmpconsent44521=CQCqRqQQCqRqQAfVwBDEA_EgAAAAAAAAAAigCkQAwARAAqAKQAAAAAA; __cmpcccu44521=aBQCsTXFgBQAzADQAGwCMAAQACAAIAAcABYAFwANAAeABQAEEAQ4AxACFgWYBMSCb0FGgKRwA1n77nmuedhFQA; _gcl_au=1.1.1372237939.1722503725; _fbp=fb.1.1722503729729.526819052739875969; campaign=top30; mf_user=7585c6c6ec6e2adfb32c4830745aecc5|; cf_clearance=YtaHqzC2PKZogvxYIn3PqdVaMJMRTulcmn7T9Ugb6qs-1722922425-1.0.1.1-Q6Yj.ps0H0V1ymZpW8R69uG8.dnn2RvBaJl81sh_w9E5U6fZwf8KXuIAj7aO.h3Majai_00iznHTO7oKDQQynA; saleschannel=organic; snst=%7B%22242%22%3A%7B%22splitname%22%3A%22id_now_bonus_flow%22%2C%22splitvariantname%22%3A%22neue+Splitvariante%22%2C%22distribution%22%3A%221%22%2C%22splitvariantid%22%3A242%7D%2C%22243%22%3A%7B%22splitname%22%3A%22id_now_bonus_flow_cookie_access%22%2C%22splitvariantname%22%3A%22neue+Splitvariante%22%2C%22distribution%22%3A%221%22%2C%22splitvariantid%22%3A243%7D%2C%223007%22%3A%7B%22splitname%22%3A%22leila2_startpage%22%2C%22splitvariantname%22%3A%22leila2_startpage_new%22%2C%22distribution%22%3A%2299%22%2C%22splitvariantid%22%3A301%7D%2C%222000%22%3A%7B%22splitname%22%3A%22best_price_logic%22%2C%22splitvariantname%22%3A%22best_price_logic%22%2C%22distribution%22%3A%221%22%2C%22splitvariantid%22%3A2000%7D%2C%223004%22%3A%7B%22splitname%22%3A%22leila2_integration%22%2C%22splitvariantname%22%3A%22release1_leila2%22%2C%22distribution%22%3A%22100%22%2C%22splitvariantid%22%3A447%7D%2C%222222%22%3A%7B%22splitname%22%3A%22wltp_feature%22%2C%22splitvariantname%22%3A%22wltp_feature%22%2C%22distribution%22%3A%221%22%2C%22splitvariantid%22%3A2222%7D%7D; _conv_v=vi%3A1*sc%3A1*cs%3A1722503717*fs%3A1722503717*pv%3A1046*exp%3A%7B100479078.%7Bv.1004191852-g.%7B%7D%7D-100479082.%7Bv.1-g.%7B%7D%7D%7D*seg%3A%7B%7D; originalLocation=https://www.sixt-neuwagen.de/konfigurieren/audi?customerType=private; sessionCount=18; LVKD=P; gtag_ga=GA1.2.2070224118.1723875327; _clck=1jwxipj%7C2%7Cfoe%7C0%7C1674; _ga=GA1.1.59857357.1723882978; _ga_K47KCJ4FFT=GS1.1.1723882978.1.0.1723883101.0.0.0; vehicleConfig=%7B%22vehicleId%22%3A%22822896920240520%22%2C%22vehicleOptions%22%3A%5B%228228969%7C1007%22%2C%228228969%7C1008%22%5D%2C%22contractType%22%3A%22VARIO%22%2C%22term%22%3A48%2C%22mileage%22%3A10000%2C%22initialPayment%22%3A%7B%22type%22%3A%22ABSOLUTE%22%2C%22amount%22%3A%220%22%7D%2C%22serviceProducts%22%3A%5B%22SUNPRO_DAMAGE_MANAGEMENT%22%5D%2C%22delivery%22%3A%7B%22paymentType%22%3A%22ONE_TIME%22%2C%22optionId%22%3A%22DEALER_PICKUP%22%2C%22deliveryType%22%3A%22DEALER_PICKUP%22%7D%2C%22vehicleNameParts%22%3A%5B%22Dacia%22%2C%22Sandero%22%2C%22Schr%C3%A4ghecklimousine%22%5D%2C%22vehicleImageUrl%22%3A%22https%3A%2F%2Fvehicle.static.prod.or.sixt-leasing.com%2FDACIA%2FSANDERO%2F2024%2FHA%2F5%2F123338b713f29826240e5bfb6b610e456c46dfd0.png%22%7D; pageviewCount=49; dicbo_id=%7B%22dicbo_fetch%22%3A1723885017050%7D; _clsk=1ro539m%7C1723885017883%7C15%7C1%7Cz.clarity.ms%2Fcollect; __cf_bm=GO7dGGOmLpcLAqO_Qg3Z0Guq4TlyK7TzJ4IIZmUmbB8-1723885023-1.0.1.1-DVdOgRwAoMe50ij9KDxebGhmcdrd6P2yjytaE1RkzMVhfqNiSQpnPAuvkxNHcRMhY_tdpgXGVOdANu0YhYEqUQ; gtag_ga_K47KCJ4FFT=GS1.2.1723882893.3.1.1723885032.0.0.0; mf_1b6d36a5-b2b0-47fb-8f39-3b8e72dbd941=1f4438c85ea639bad45c55944a9fb727|081722813714cfff0b52edd1f80236618eb9aac2.7553023213.1723883062682$081726930a467c4a1ea77d6adf212b7b38185944.2652562946.1723883066495$08172905318498e2df823683f098830a8ec62a74.-603121347.1723883069707$08175086b02915c0dda04521cce1c410507abd1a.-603121347.1723883150389$08170050326fa40a20e41ef45d6bfae92a2256ce.-603121347.1723883280653$0817565939fd4bde3f2e556a6b99fcca62c1b042.47.1723885016164|1723885045961|900359224_-314497661|14||||1|18.10|1.17588',
        'pragma': 'no-cache',
        'priority': 'u=0, i',
        'sec-ch-ua': '"Not)A;Brand";v="99", "Google Chrome";v="127", "Chromium";v="127"',
        'sec-ch-ua-arch': '"x86"',
        'sec-ch-ua-bitness': '"64"',
        'sec-ch-ua-full-version': '"127.0.6533.120"',
        'sec-ch-ua-full-version-list': '"Not)A;Brand";v="99.0.0.0", "Google Chrome";v="127.0.6533.120", "Chromium";v="127.0.6533.120"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-model': '""',
        'sec-ch-ua-platform': '"Windows"',
        'sec-ch-ua-platform-version': '"10.0.0"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
    }

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, headers=self.headers, cookies=self.cookies, callback=self.url_navigation)

    def url_navigation(self, response):

        results = response.css("h2[data-e2e='cc-num-results']::text").get().strip().split(' ')[0]
        url = f"https://www.sixt-neuwagen.de/konfigurieren?customerType=private&limit={results}"

        yield scrapy.Request(url=url, headers=self.headers, cookies=self.cookies, callback=self.url_info, meta={'limit':results})

    def url_info(self,response):

        data = json.loads(response.css('script[id="web-newcar-state"]::text').get().strip())
        value = data[f"G.json.{{bff}}/pages/configurator/index?customerType=PRIVATE&limit={response.meta['limit']}&portal=newcar&tierId=2"]['body']['hits']

        for val in value:
            make = val['makeId'].lower()
            model = val['modelId'].lower()
            id = val['id']

            url = f"https://www.sixt-neuwagen.de/konfigurieren/node/speedy-configurator?contractType=LEASING&customerType=PRIVATE&deliverableStatus=yes&id={id}&makeLocalNameSlug={make}&modelLocalNameSlug={model}"

            yield scrapy.Request(url=url, headers=self.headers, cookies=self.cookies, callback=self.product_url)
            break ###

    def product_url(self,response):

        data = json.loads(response.text)

        data = data['availableFilters']['vehicleId']
        for val in data:
            make = val['makeLocalNameSlug'].lower()
            model = val['modelLocalNameSlug'].lower()
            body = val['bodyLocalNameSlug'].lower()
            id = val['id']
            amount = 0
            customers = ['BUSINESS', 'PRIVATE']
            leasing_type = ['VARIO', 'LEASING']
            terms = [30, 36, 42, 48, 54, 60]  # 60 not included in vario leasing
            mileages = [30000, 35000, 40000, 45000.50000, 55000,60000]  # 60,000 not included in vario leasing

            for customer in customers:
                for leasing in leasing_type:

                    if leasing == 'VARIO':

                        mod_terms = terms[0:len(terms)-1] if leasing == 'VARIO' else terms
                        mod_mileages = mileages[0:len(mileages)-1] if leasing == 'VARIO' else mileages

                        for term in mod_terms:
                            for mileage in mod_mileages:
                                url = f"https://www.sixt-neuwagen.de/konfigurieren/node/speedy-configurator?bodyLocalNameSlug={body}&contractType={leasing}&customerType={customer}&initialPayment[amount]={amount}&initialPayment[type]=ABSOLUTE&makeLocalNameSlug={make}&mileage={mileage}&modelLocalNameSlug={model}&term={term}&vehicleId={id}"
                                yield scrapy.Request(url=url, headers=self.headers, cookies=self.cookies,callback=self.parse,meta={'item_type': 'product'})
                #                 break
                #             break
                #     break
                # break
            break


    def parse(self, response):

        data = json.loads(response.text)

        item = response.meta.get('item', VehicleItem())

        # Car Information
        item['Make'] = data['config']['makeLocalNameSlug']
        item['Model'] = data['config']['modelLocalNameSlug']
        item['Body_Type'] = data['config']['bodyLocalNameSlug']
        item['Number_Of_Doors'] = data['target']['doors']
        derivative = data['target']['localName']
        item['Derivative'] = derivative
        item['Derivative_Translated_English'] = derivative
        item['Trim'] = derivative.split(' ')[-1]
        item['Power_Train'] = data['target']['powerTrainName']
        item['Version_Name'] = f"{data['config']['makeLocalNameSlug']} {data['config']['modelLocalNameSlug']} {derivative.split(' ')[-1]} {derivative} {data['target']['transmissionTypeLocalName']} {data['target']['doors']} {data['target']['powerTrainName']} {data['target']['bodyLocalName']}"

        item['Version_Name_Translated_English'] = f"{data['target']['makeLocalName']} {data['target']['modelLocalName']} {derivative.split(' ')[-1]} {derivative} {data['target']['transmissionType']} {data['target']['doors']} {data['target']['powerTrainName']} {data['target']['bodyLocalNameSlug']}"

        # Other information
        item['Customer_Type'] = data['config']['customerType']
        item['Product_Name'] = data['config']['contractType']
        item['Data_Source'] = 'market'
        item['Other_Sources'] = 'market'
        item['Currency'] = 'Euro'
        item['Country'] = 'germany'

        # Product url
        product_url_trim = re.findall(r'\b[A-Z][a-z]+\b', derivative)
        url_trim = ''
        for url_trim_val in product_url_trim:
            url_trim += url_trim_val + '-'
        url_trim = url_trim[0:-1]

        product_url = f"https://www.sixt-neuwagen.de/konfigurieren/{data['config']['makeLocalNameSlug'].lower()}/{data['config']['modelLocalNameSlug'].lower()}/{data['config']['bodyLocalNameSlug'].lower()}/{url_trim.lower()}/{data['target']['id']}/farbe?customerType={data['config']['customerType'].lower()}"
        item['Web_Source_Url'] = product_url
        item['Advertised_Price_Point_Monthly_Payment'] = data['target']['environmentalBonusAvailable']

        # Finance information
        item['Contract_Duration_Months'] = data['config']['term']
        item['Of_Monthly_Instalments'] = data['config']['term']
        item['Yearly_Mileage_Km'] = data['config']['mileage']
        item['Yearly_Mileage_Miles'] = data['config']['mileage'] * 0.621371
        item['Total_Contract_Mileage_Km'] = ( int(data['config']['mileage']) * (int(data['config']['term']) / 12) )
        item['Total_Contract_Mileage_Miles'] = (int(data['config']['mileage']) * 0.621371) * (int(data['config']['term']) / 12)
        item['Deposit_Percentage_Of_Price'] = 0
        finance = data['calculations'][data['config']['contractType']]
        item['Price'] = finance['basePrice']
        item['Sourced_Financed_Amount_Percentage_Of_Price'] = (finance['totalAmount'] / finance['basePrice']) * 100
        item['Final_Payment_Percentage_Of_Price'] = (finance['finalPayment'] / finance['basePrice']) * 100

        if data['config']['customerType'] == 'PRIVATE':
            item['Deposit_Base'] = 0
            item['Regular_Monthly_Instalment_Amount_Base'] = data['target']['minRate']
            item['Sourced_Financed_Amount_Base'] = finance['totalAmount']
            item['Final_Payment_Base'] = finance['finalPayment']
        else:
            item['Deposit_Retail'] = 0
            item['Regular_Monthly_Instalment_Amount_Retail'] = data['target']['minRate']
            item['Delivery_Costs_Retail'] = finance['logisticCosts']
            item['Sourced_Financed_Amount_Retail'] = finance['totalAmount']
            item['Final_Payment_Retail'] = finance['finalPayment']

        insurance_url = f"https://www.sixt-neuwagen.de/konfigurieren/node/serviceproducts?term={data['config']['term']}&tierId=2&vehicleId={data['config']['vehicleId']}&mileage={data['config']['mileage']}&contractType={data['config']['contractType']}&customerType={data['config']['customerType']}&jatoUniqueId={int(int(data['config']['vehicleId'])/100000000)}"
        yield scrapy.Request(url=insurance_url, headers=self.headers, cookies=self.cookies, callback=self.services_parse,meta={'customer' : data['config']['customerType'],'item_type': 'service','item':item})


    def services_parse(self, response):

        item = response.meta.get('item', VehicleItem())

        assistance = json.loads(response.text)[0]
        item['Road_Assistance'] = assistance['description']
        item['Road_Assistance_Description'] = assistance['description']
        item['Repair'] = assistance['additionalInformation']
        item['Repair_Description'] = assistance['additionalInformation']
        item['Courtesy_Car'] = assistance['additionalInformation']
        item['Courtesy_Car_Description'] = assistance['additionalInformation']

        maintenance_data = json.loads(response.text)[3]
        item['Maintenance'] = maintenance_data['name']
        item['Maintenance_Description'] = maintenance_data['description']
        item['Maintenance_Amount'] = maintenance_data['rate']['netAmount']

        insurance = json.loads(response.text)[2]
        item['Insurance'] = insurance['rate']['netAmount']
        item['Insurance_Description'] = insurance['rate']['netAmount']
        item['Monthly_Payment_Provider_Name'] = insurance['additionalInformation']

        tyre_data = json.loads(response.text)[4]
        item['Tyres'] = tyre_data['name']
        item['Tyres_Description'] = tyre_data['description']
        item['Tyres_Amount'] = tyre_data['rate']['netAmount']

        contract_url = f"https://www.sixt-neuwagen.de/_next/data/f5XZ0eq3jnWvrXF5WQqih/faq/rueckgabe.json?slug=faq&slug=rueckgabe&customerType={response.meta['customer'].lower()}"

        yield scrapy.Request(url=contract_url, headers=self.headers, cookies=self.cookies, callback=self.contract_parse,meta={'customer' : response.meta['customer'],'item_type': 'contract','item':item})

    def contract_parse(self,response):

        data = json.loads(response.text)

        item = response.meta.get('item', VehicleItem())
        if response.meta['customer'] != 'PRIVATE':
            item['Cost_To_Return_The_Vehicle_Retail'] = data['pageProps']['content']['sections'][1]['entity']['faqItems'][1]['entity']['answerBody']['processed']

        yield item

