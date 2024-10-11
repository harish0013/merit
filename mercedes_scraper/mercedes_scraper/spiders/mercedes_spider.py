import scrapy
import json
import pandas as pd
import os

class MercedesSpider(scrapy.Spider):
    name = 'mercedes'

    # List of URLs for different vehicle variants
    start_urls = [
        'https://bos-api.vds.corpinter.net/api/public/vehicle/8354360916',  # Variant 1
        'https://bos-api.vds.corpinter.net/api/public/vehicle/8354360985',  # Variant 2
        'https://bos-api.vds.corpinter.net/api/public/vehicle/8354361080',  # Variant 3
        'https://bos-api.vds.corpinter.net/api/public/vehicle/8354360747'   # Variant 4
    ]

    headers = {
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9',
        'cache-control': 'no-cache',
        'origin': 'https://www.mercedes-benz.it',
        'pragma': 'no-cache',
        'priority': 'u=1, i',
        'referer': 'https://www.mercedes-benz.it/passengercars/buy/new-car/search-results.html/?emhsortType=name-desc&emhvehicleCategory=new-passenger-cars&emhmodelIdentifier=EQT_CLASS',
        'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'cross-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
    }

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(
                url=url,
                headers=self.headers,
                callback=self.parse
            )

    def parse(self, response):
        try:
            # Load the JSON response
            data = json.loads(response.text)

            # Extract fields from the JSON response
            vehicle_data = data.get('data', {}).get('vehicleData', {})
            price_data = vehicle_data.get('price', {})
            emission_data = vehicle_data.get('emission', {})

            # Extracting data based on provided JSON structure
            make = vehicle_data.get('brand', 'Not Available')
            model = vehicle_data.get('model', {}).get('it', 'Not Available')
            trim = vehicle_data.get('name', {}).get('it', 'Not Available')
            derivative = f"{vehicle_data.get('engine', [{}])[0].get('power', 'Not Available')} HP, {vehicle_data.get('engineData', {}).get('driveConcept', 'Not Available')}"
            derivative_translated = 'Not Available'
            number_of_doors = vehicle_data.get('numberDoors', 'Not Available')
            body_type = vehicle_data.get('bodyType', {}).get('it', 'Not Available')
            power_train = vehicle_data.get('engineData', {}).get('driveConcept', 'Not Available')
            version_name = f"{make} {model} {trim} {derivative} {body_type}"
            version_name_translated = 'To be translated'
            manufacturer_code = vehicle_data.get('fdk', 'Not Available')
            configurator_model_year = 'To be Checked in Backend'
            uid = data.get('data', {}).get('objectId', 'NA')
            data_date = 'NA'
            conclude_date = 'NA'
            version_availability = 'Available' if vehicle_data.get('available', False) else 'Not Available'
            currency = price_data.get('priceCurrency', 'EUR')
            price = price_data.get('listRoadPriceTotal', 'Not Available')
            delivery_costs_msrp = price_data.get('local', {}).get('deliveryCost', 'Not Available')
            other_mandatory_costs = 'Not Available'
            country = vehicle_data.get('market', 'Not Available')
            research_date = 'Not Available'
            start_date = 'NA'
            end_date = 'NA'
            customer_type = 'Private'
            monthly_payment_type = 'Not Available'
            product_name = vehicle_data.get('name', {}).get('it', 'Not Available')
            product_description = 'To be left blank'
            monthly_payment_provider_name = 'Not Available'
            monthly_payment_provider_type = 'Not Available'
            interest_rate = 'Not Available'
            rate_type = 'APR'
            contract_duration_months = 'Not Available'
            yearly_mileage_km = 'Not Available'
            yearly_mileage_miles = 'To be calculated'
            total_contract_mileage_km = 'To be calculated'
            total_contract_mileage_miles = 'To be calculated'
            deposit_percent_price = 'Not Available'
            deposit_msrp = 'Not Available'
            deposit_base = 'Not Available'
            num_monthly_instalments = 'Not Available'
            first_monthly_instalment_amount_msrp = 'Not Available'
            monthly_instalment_amount_msrp = 'Not Available'
            additional_fees_msrp = 'Not Available'
            additional_fees_base = 'Not Available'
            final_payment_type = 'Not Available'
            final_payment_percent_price = 'Not Available'
            final_payment_msrp = 'Not Available'
            final_payment_base = 'Not Available'
            data_source = 'Market'
            web_source_url = response.url
            oem_web_financial_configurator_source = 'Not Available'
            captive_financial_configurator_source = 'Not Available'
            non_captive_financial_config_source = 'Not Available'
            bank_financial_configurator_source = 'Not Available'
            sourced_dealer_quote = 'NA'
            jato_internal_source = 'NA'
            other_sources = 'Not Available'
            vehicle_price_reference = 'On road price'
            mandatory_dealer_contribution_percent_price = 'Not Available'
            mandatory_dealer_contribution_msrp = 'Not Available'
            mandatory_dealer_contribution_base = 'Not Available'
            oem_discount_percent_price = 'Not Available'
            oem_discount_msrp = 'Not Available'
            oem_discount_base = 'Not Available'
            government_contribution_percent_price = 'Not Available'
            government_contribution_msrp = 'Not Available'
            government_contribution_base = 'Not Available'
            downpayment_allowance_percent_price = 'Not Available'
            downpayment_allowance_msrp = 'Not Available'
            downpayment_allowance_base = 'Not Available'
            residual_value_percent_price = 'Not Available'
            residual_value_msrp = 'Not Available'
            residual_value_base = 'Not Available'
            insurance = 'N'
            sourced_financed_amount_percent_price = 'To be calculated'
            sourced_financed_amount_msrp = 'Not Available'
            sourced_financed_amount_base = 'Not Available'
            unique_id = 'NA'
            change_status = 'NA'
            updates_column = 'NA'
            back_end_data = 'NA'
            vehicle_hash = 'NA'

            # Create DataFrame with specified headers
            df = pd.DataFrame([{
                'Make': make,
                'Model': model,
                'Trim': trim,
                'Derivative': derivative,
                'Derivative - Translated (English)': derivative_translated,
                'Number of Doors': number_of_doors,
                'Body Type': body_type,
                'Power Train': power_train,
                'Version name': version_name,
                'Version name - Translated (English)': version_name_translated,
                'Manufacturer\'s code': manufacturer_code,
                'Configurator Model Year': configurator_model_year,
                'uid': uid,
                'data date': data_date,
                'conclude date': conclude_date,
                'version availability': version_availability,
                'Currency': currency,
                'Price': price,
                'Delivery Costs - MSRP': delivery_costs_msrp,
                'Other mandatory costs': other_mandatory_costs,
                'Country': country,
                'Research date': research_date,
                'start date': start_date,
                'end date': end_date,
                'Customer type': customer_type,
                'Monthly payment type': monthly_payment_type,
                'Product name': product_name,
                'Product description': product_description,
                'Monthly payment provider name': monthly_payment_provider_name,
                'monthly payment provider type': monthly_payment_provider_type,
                'Interest rate': interest_rate,
                'Rate type': rate_type,
                'Contract duration (months)': contract_duration_months,
                'Yearly Mileage (Km)': yearly_mileage_km,
                'Yearly Mileage (miles)': yearly_mileage_miles,
                'Total contract mileage (Km)': total_contract_mileage_km,
                'Total contract mileage (miles)': total_contract_mileage_miles,
                'Deposit (% of price)': deposit_percent_price,
                'Deposit - MSRP': deposit_msrp,
                'Deposit - Base': deposit_base,
                '# of monthly instalments': num_monthly_instalments,
                'First monthly instalment amount - MSRP': first_monthly_instalment_amount_msrp,
                'Monthly instalment amount - MSRP': monthly_instalment_amount_msrp,
                'Additional fees - MSRP': additional_fees_msrp,
                'Additional fees - Base': additional_fees_base,
                'Final payment type': final_payment_type,
                'Final payment (% of price)': final_payment_percent_price,
                'Final payment - MSRP': final_payment_msrp,
                'Final payment - Base': final_payment_base,
                'Data source': data_source,
                'Web source url': web_source_url,
                'OEM web financial configurator source': oem_web_financial_configurator_source,
                'Captive financial configurator source': captive_financial_configurator_source,
                'Non-captive financial config source': non_captive_financial_config_source,
                'Bank financial configurator source': bank_financial_configurator_source,
                'Sourced dealer quote': sourced_dealer_quote,
                'JATO internal source': jato_internal_source,
                'Other sources': other_sources,
                'Vehicle price reference': vehicle_price_reference,
                'Mandatory dealer contribution (% of price)': mandatory_dealer_contribution_percent_price,
                'Mandatory dealer contribution - MSRP': mandatory_dealer_contribution_msrp,
                'Mandatory dealer contribution - Base': mandatory_dealer_contribution_base,
                'OEM discount (% of price)': oem_discount_percent_price,
                'OEM discount - MSRP': oem_discount_msrp,
                'OEM discount - Base': oem_discount_base,
                'Government contribution (% of price)': government_contribution_percent_price,
                'Government contribution - MSRP': government_contribution_msrp,
                'Government contribution - Base': government_contribution_base,
                'Downpayment allowance (% of price)': downpayment_allowance_percent_price,
                'Downpayment allowance - MSRP': downpayment_allowance_msrp,
                'Downpayment allowance - Base': downpayment_allowance_base,
                'Residual value - % of price': residual_value_percent_price,
                'Residual value - MSRP': residual_value_msrp,
                'Residual value - Base': residual_value_base,
                'Insurance': insurance,
                'Sourced financed amount (% of price)': sourced_financed_amount_percent_price,
                'Sourced financed amount - MSRP': sourced_financed_amount_msrp,
                'Sourced financed amount - Base': sourced_financed_amount_base,
                'Unique ID': unique_id,
                'Change Status': change_status,
                'Updates Column': updates_column,
                'Back-end data': back_end_data,
                'vehicle_hash': vehicle_hash
            }])

            # Save DataFrame to CSV
            csv_file = 'scrap.csv'
            df.to_csv(csv_file, mode='a', header=not os.path.isfile(csv_file), index=False)

        except json.JSONDecodeError:
            self.log('Failed to decode JSON from response: %s' % response.url)
        except Exception as e:
            self.log(f'Error occurred: {str(e)}')
