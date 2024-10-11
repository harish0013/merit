import scrapy

class FlipkartLaptopsSpider(scrapy.Spider):
    name = "flipkart_laptops"
    allowed_domains = ["flipkart.com"]
    start_urls = ["https://www.flipkart.com/search?q=laptops"]

    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
    }

    cookies = {
        'T': 'TI172076333197400128612326774303110095296959658745682175520977939689',
        'rt': 'null',
        'K-ACTION': 'null',
        'ud': '7._EA8MPay8RgQCnXpsBXZHK5sc7gILo9FHj0aYgGHR1Oumr39zAo6t-7vuMSHXlmkUuxx5a6dthHiykOKVmj8-wOzBa8u4gZzHlhFy3uw4bvUy_JKJfpVN--Qg-8o1yjiZUY9HMR_NWT0zqe9hU78qQ',
        '_pxvid': '6be344d2-4012-11ef-8efe-92cbc6e95587',
        'at': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImQ2Yjk5NDViLWZmYTEtNGQ5ZC1iZDQyLTFkN2RmZTU4ZGNmYSJ9.eyJleHAiOjE3MjMzNTg1MTcsImlhdCI6MTcyMTYzMDUxNywiaXNzIjoia2V2bGFyIiwianRpIjoiZWNjZjAzNTgtYTNjOS00NDcxLTliODAtODU2OGExY2U1NGFkIiwidHlwZSI6IkFUIiwiZElkIjoiVEkxNzIwNzYzMzMxOTc0MDAxMjg2MTIzMjY3NzQzMDMxMTAwOTUyOTY5NTk2NTg3NDU2ODIxNzU1MjA5Nzc5Mzk2ODkiLCJrZXZJZCI6IlZJREVGQzU1QTAxNkYzNDBFQjg1NDk3Q0RBMDMxOEZCNjAiLCJ0SWQiOiJtYXBpIiwidnMiOiJMTyIsInoiOiJIWUQiLCJtIjp0cnVlLCJnZW4iOjR9.HlwCk6XrL71riH2adOd39jdTf_rkpueg-idtDM1uHLE',
        'vw': '1280',
        'dpr': '1.5',
        'vh': '332',
        'AMCV_17EB401053DAF4840A490D4C%40AdobeOrg': '-227196251%7CMCIDTS%7C19929%7CMCMID%7C49431364109942220852284183760756192422%7CMCAAMLH-1722235320%7C12%7CMCAAMB-1722419240%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1721821640s%7CNONE%7CMCAID%7CNONE',
        'qH': 'c06ea84a1e3dc3c6',
        'S': 'd1t14Pz8/Dg8/Pz92P3paAkY/P0kkMiQYX3Nu/5jweKvpHR/6DYrUWQ04sDeE6IpYEx+q8ie29b/Rd8/GwMS6tUJZEw==',
        'vd': 'VIDEFC55A016F340EB85497CDA0318FB60-1720763334189-5.1721888489.1721888489.155424657',
        'Network-Type': '4g',
        '_px3': 'dac30475a089bc20f34c432d208840c7b11ed23857354dd100606807e8e501d3:qomVyh79PBMab7sD4GNIABdjEQhUr/WAJOT+YXLKFSKqacbzOZAW/6BRXp75iA4NlT/M4jKB4FM/SYmLUGJ1kA==:1000:5UiS1DaN/AeWt5XXPyPXUXppvIXptL7ObAVy69rreq7MvDAItWjDVGUwObtEvNqdtQ12tw9hxcgtSKKFn6QU1KAX67zrM/4lWygtCPFPX/KibXSJwiUEcfTsIcUkacw4BtDGoHAJkrXEW0LFc8NaAIC3wF0jKQRQH91Os8xpFfSV8O3dxZSKA0rCATZqbfUXlYETMHh0o4G0xN0wj4ZkIO3cVr3PD0HPpCPVl19HGek=',
        'SN': 'VIDEFC55A016F340EB85497CDA0318FB60.TOK64794F84B36747739E6520B17C44FE83.1721888537.LO',
    }

    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Language': 'en-US,en;q=0.9',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Pragma': 'no-cache',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
        'sec-ch-ua-arch': '"x86"',
        'sec-ch-ua-full-version': '"126.0.6478.183"',
        'sec-ch-ua-full-version-list': '"Not/A)Brand";v="8.0.0.0", "Chromium";v="126.0.6478.183", "Google Chrome";v="126.0.6478.183"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-model': '""',
        'sec-ch-ua-platform': '"Windows"',
        'sec-ch-ua-platform-version': '"10.0.0"',
    }

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url, callback=self.parse, headers=self.headers, cookies=self.cookies)

    def parse(self, response):
        # Extract product information
        for product in response.css('div.tUxRFH'):
            yield {
                'name': product.css('div.KzDlHZ::text').get(),
                'price': product.css('div.Nx9bqj._4b5DiR::text').get(),
                'rating': product.css('div.XQDdHH::text').get(),
                'reviews': product.css('span.Wphh3N span span::text').getall()[2]
            }

        # # Handle pagination
        # next_page = response.css('nav.WSL9JP::attr(href)').get()
        # if next_page:
        #     next_page_url = response.urljoin(next_page)
        #     yield scrapy.Request(next_page_url, callback=self.parse, headers=self.headers, cookies=self.cookies)
