import scrapy

class SnapdealShoesSpider(scrapy.Spider):
    name = "snapdeal_shoes"
    allowed_domains = ["snapdeal.com"]
    start_urls = [
        "https://www.snapdeal.com/products/mens-footwear-sports-shoes?sort=plrty"
    ]

    def start_requests(self):
        # Define the cookies
        cookies = {
            'versn': 'v1',
            'u': '172188554825585725',
            'sd.zone': 'NO_ZONE',
            'xg': '"eyJ3YXAiOnsiYWUiOiIxIn0sIm1hcGkiOnsiY2RuX3MiOiIxIn0sInNjIjp7InJ0b21vZGVsIjoiQyIsInBkZCI6Im1sMCJ9LCJwcyI6eyJhdCI6Im8ifSwidWlkIjp7Imd1aWQiOiI5Mzg3YTdiMy1lMzVmLTQwNDUtYjdlOS03YjE2NjY1OWU3YTUifX18fDE3MjE4ODczNDgyNjY="',
            'xc': '"eyJ3YXAiOnsiYWUiOiIxIn0sIm1hcGkiOnsiY2RuX3MiOiIxIn0sInNjIjp7InJ0b21vZGVsIjoiQyIsInBkZCI6Im1sMCJ9LCJwcyI6eyJhdCI6Im8ifX0="',
            'SCOUTER': 'x49vqf8krv5eor',
            'JSESSIONID': '8123D500B4B27F9974D21A9515D97D01',
            'alps': 'akm',
            '_gcl_au': '1.1.975017373.1721885549',
            '__rtbh.lid': '%7B%22eventType%22%3A%22lid%22%2C%22id%22%3A%22eKUoi0bSIz2uskXsh1eM%22%7D',
            'isWebP': 'true',
            '__rtbh.uid': '%7B%22eventType%22%3A%22uid%22%2C%22id%22%3A%229387a7b3-e35f-4045-b7e9-7b166659e7a5%22%7D',
            'st': 'utm_source%3DSEO%7Cutm_content%3Dnull%7Cutm_medium%3Dnull%7Cutm_campaign%3Dnull%7Cref%3Dnull%7Cutm_term%3Dnull%7Caff_id%3Dnull%7Caff_sub%3Dnull%7Caff_sub2%3Dnull%7C',
            'vt': 'utm_source%3DSEO%7Cutm_content%3Dnull%7Cutm_medium%3Dnull%7Cutm_campaign%3Dnull%7Cref%3Dnull%7Cutm_term%3Dnull%7Caff_id%3Dnull%7Caff_sub%3Dnull%7Caff_sub2%3Dnull%7C',
            'lt': 'utm_source%3DSEO%7Cutm_content%3Dnull%7Cutm_medium%3Dnull%7Cutm_campaign%3Dnull%7Cref%3Dnull%7Cutm_term%3Dnull%7Caff_id%3Dnull%7Caff_sub%3Dnull%7Caff_sub2%3Dnull%7C',
            '_fbp': 'fb.1.1721885551052.523942861174692971',
            'sdCPW': 'false',
            '_sdDPPageId': '1721885564455_3960_172188554825585725',
            'hpcl': '255',
            '_uetsid': '492a51c04a4711ef8d269b1f68f9711b',
            '_uetvid': '492a5f404a4711efba260db731249a79',
            's_pers': '%20s_vnum%3D1724477550548%2526vn%253D1%7C1724477550548%3B%20gpv_pn%3DallProducts%253Ahttps%253A%252F%252Fwww.snapdeal.com%252Fproduct%252Fcampus-rang-orange-mens-sports%252F5764608159962894291%7C1721887364904%3B%20s_invisit%3Dtrue%7C1721887364906%3B',
            's_sess': '%20s_cc%3Dtrue%3B%20s_sq%3D%3B%20s_ppv%3D29%3B',
            'cto_bundle': 'ej4BMl9ZJTJCQld0TEFVbzZxM0t1aVowWUslMkI3S1B2SkY3VElRb2FDUUx5alpZUFdUN0J1dnNBZTREdGpTdFMweFRXJTJGTVBlWURiY1dmejdxbHN2RlU0ckRjYkRsVk84Qng0WUtwQ2lrWnhiaDFERjNWQTNhOUhQcmNrMjFNaEFqVzVaUFpHZ3daVlZIZXFLUWpjYUpMWXhUZGpDd1FPVXNrU2MzUExleDlnTnM4aGpXU2ljZmdCdlFJOWRmc1J1WjNSTEE0bWElMkJVaFp0akc5dUNrZGs1TCUyRlhhOEVhQSUzRCUzRA',
            'AWSALB': '5CU1LmXGGY0XqXqpkwl0VpQoxunoa9dB6UvTSp5PAjgO+fIuUjTzXAg6iCfEqnB8cKxtwEhnH6U4zAnVOkU11NCCQmYB1pL6qxZIEWYg437ad/VZ/GaAA7aCsdh5',
            'AWSALBCORS': '5CU1LmXGGY0XqXqpkwl0VpQoxunoa9dB6UvTSp5PAjgO+fIuUjTzXAg6iCfEqnB8cKxtwEhnH6U4zAnVOkU11NCCQmYB1pL6qxZIEWYg437ad/VZ/GaAA7aCsdh5',
            '_sdRefPgCookie': '%7B%22refPg%22%3A%22categoryListing%22%2C%22refPgId%22%3A%221721885564455_3960_172188554825585725%22%7D',
            '_sdRefEvtCookie': '%7B%22refEvt%22%3A%22eventLoggingLogging%22%2C%22refEvtId%22%3A%221721885564946_6213_172188554825585725%22%7D',
        }

        # Define the headers
        headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-language': 'en-US,en;q=0.9',
            'cache-control': 'no-cache',
            'pragma': 'no-cache',
            'priority': 'u=0, i',
            'referer': 'https://www.snapdeal.com/',
            'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
        }

        for url in self.start_urls:
            yield scrapy.Request(url=url, cookies=cookies, headers=headers, callback=self.parse)

    def parse(self, response):
        for product in response.css('div.col-xs-6.favDp.product-tuple-listing.js-tuple '):
            yield {
                'name': product.css('p.product-title::text').get(),
                'price': product.css('span.lfloat.product-price::text').get(),
                'original_price': product.css('span.lfloat.product-desc-price.strike::text').get(),
                'discount': product.css('div.product-discount span::text').get(),
                'image': product.css('picture.picture-elem source::attr(srcset)').get(),
            }

        # next_page = response.css('div.show-more.btn.btn-line.btn-theme-secondary::text').getall()
        # if next_page:
        #     yield response.follow(next_page, self.parse)


