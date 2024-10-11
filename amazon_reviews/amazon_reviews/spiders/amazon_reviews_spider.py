import scrapy
from scrapy.http import Request

class AmazonReviewsSpider(scrapy.Spider):
    name = "amazon_reviews"
    allowed_domains = ["amazon.in"]
    start_urls = ['https://www.amazon.in/Apple-iPhone-Pro-Max-256/product-reviews/B0CHWV2WYK/ref=cm_cr_dp_d_show_all_btm?ie=UTF8&reviewerType=all_reviews']

    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'FEED_FORMAT': 'csv',
        'FEED_URI': 'reviews.csv',
        'FEED_EXPORT_FIELDS': ['review_title', 'review_author', 'review_date', 'review_text', 'review_rating', 'review_helpful'],
        'DOWNLOAD_DELAY': 3,
        'CONCURRENT_REQUESTS': 1,
        'RETRY_TIMES': 10,
        'RETRY_HTTP_CODES': [500, 502, 503, 504, 522, 524, 408],
        'COOKIES_ENABLED': True,
    }

    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
        'cache-control': 'no-cache',
        'device-memory': '8',
        'downlink': '3.25',
        'dpr': '1.5',
        'ect': '4g',
        'pragma': 'no-cache',
        'priority': 'u=0, i',
        'rtt': '50',
        'sec-ch-device-memory': '8',
        'sec-ch-dpr': '1.5',
        'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-ch-ua-platform-version': '"10.0.0"',
        'sec-ch-viewport-width': '1280',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
        'viewport-width': '1280',
    }

    cookies = {
        'session-id': '258-5924374-4604052',
        'i18n-prefs': 'INR',
        'ubid-acbin': '257-4696915-1283608',
        'lc-acbin': 'en_IN',
        'x-acbin': '"WNSUcTZ?g99UX22JOovBbifzVoj7mB65EhXiuoTSp4xnD3R9LYvjURDj7lVwX5JL"',
        'at-acbin': 'Atza|IwEBIPmOQkoXtcGSiYGj8cmrqxpLE11qAaf1UyD2Dc3aBmVLfzHPoi6LScW_e6Xi9DSCj-syeaRhqsWM8eQi23l0LiZ1Ye5H1EnR1Gdhs-nhbWx06IikrAeJ3jGZC-8Q8wYs04ZOJpPE5ZxlAop9r24xl7rSfysvBJqdV4SXsT9pndOHGe-8PZTAw2bC9mNXD3XIr6RYQ4rvl4bm0oHYi8hNEkr1z5D7tK3AGAu6qLoXEpaMOQ',
        'sess-at-acbin': '"eVUqFfYIf6ZSaQeyGe+pMywrZBnbRTf56UvuIF65WQE="',
        'sst-acbin': 'Sst1|PQHUf5AZc1Ym0Ayj81SYoejkCfsI5Y0p2mAtLkKX_ftPYM7SeXt2iia1_Qx9U8S-E8ue8NJtnBgfzv8LRH2OreZlK0aPSvYPELCIomiRjORBS2Y8wS70Y51o3L-Ng_EVMruLjEFIrR5vG0OAvdHFwv5tYKVMTEMPphV4oom9dANiaDaqxLcytEEVtKkrXQ55R3-AJ3T8nVWRdX3WKPgbRHdwI_eUo1fMm99WS7ew9U-11epySxW-19cMmzfLO5VzbGid7DDYDGISL8QLeQ5Fl72rvqBS9ZbHFAxI-hhApcScvMc',
        's_vnum': '2153214184775%26vn%3D1',
        's_nr': '1721214241091-New',
        's_dslv': '1721214241092',
        'session-id-time': '2082787201l',
        'session-token': 'dWX0CzcoKpUw/bxd0nqfdTJgOdF+8991KbM/27ATptCg/SM3DPBLrgsZEtxT0gGSE7FExvXqzdpkE8uAnR//6iADiyR3A+Cj+arR45fgDt9EYWq/D3OSO7DKog/qTWNgujsdslEVq0LkyltYH74lk8FaLk1WQt4DIGbnqi+MpOVOBGkjhJo7KtCyewrJYM637f+IZ9yMuBFsLcHkLUpL4liwtF8Wbq+va/mPLQLWnrpSSqbLkHp6cKQoHfUfV7NZcj9vWidYBl/RZjxBrnju2iihLj/Z/vP6B6rb6J7oiaHHDOCrJZTrEQantT9xM5MJ7Goh0BN8yHurmSjc3zdyAsatzcgsxoSVJ4cOx1AdxVNMatPZfVkMDrQvXAX9naII',
        'csm-hit': 'tb:48YYQE0NXJWEKWGA7MCV+s-48YYQE0NXJWEKWGA7MCV|1721714602342&t:1721714602342&adb:adblk_no',
    }

    def start_requests(self):
        # headers = {
        #     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        #     'Accept-Language': 'en-US,en;q=0.9',
        #     'Accept-Encoding': 'gzip, deflate, br',
        #     'Referer': 'https://www.amazon.in/',
        #     'DNT': '1',
        #     'Connection': 'keep-alive',
        #     'Upgrade-Insecure-Requests': '1',
        # }
        # cookies = {
        #     '_bb_lat_long': 'MTIuOTM2OTgwM3w4MC4xNzQwMjAy',  # Example cookie; replace with actual values
        # }
        for url in self.start_urls:
            yield Request(url, headers=self.headers, cookies=self.cookies, callback=self.parse)

    def parse(self, response):
        # Follow the link to all reviews
        all_reviews_link = response.css('a[data-hook="see-all-reviews-link-foot"]::attr(href)').get()
        if all_reviews_link:
            full_url = response.urljoin(all_reviews_link)
            yield Request(full_url, callback=self.parse_reviews, headers=response.request.headers, cookies=response.request.cookies)
        else:
            # Parse the current page reviews
            yield from self.parse_reviews(response)

    def parse_reviews(self, response):
        reviews = response.css('div[data-hook="review"]')
        for review in reviews:
            yield {
                'review_title': review.css('a.a-size-base.a-link-normal.review-title.a-color-base.review-title-content.a-text-bold span::text').getall()[1],
                'review_author': review.css('span.a-profile-name::text').get(),
                'review_date': review.css('span.review-date::text').get(),
                'review_text': " ".join(review.css('span.review-text span::text').getall()),
                'review_rating': review.css('i.review-rating span::text').get(),
                'review_helpful': review.css('span.cr-vote span::text').get(),
            }

        # Extract next page link
        next_page = response.css('li.a-last a::attr(href)').get()
        yield {'next': next_page}
        if next_page:
            full_next_page_url = response.urljoin(next_page)
            yield Request(full_next_page_url, callback=self.parse_reviews, headers=response.request.headers, cookies=response.request.cookies)
