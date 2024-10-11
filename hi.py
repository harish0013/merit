import requests

def fetch_product_details(pincode, lat_long_cookie):
    # URL from which to fetch data
    url = "https://www.bigbasket.com/listing-svc/v2/products"

    # Cookies and headers
    cookies = {
        'x-entry-context-id': '100',
        'x-entry-context': 'bb-b2c',
        '_bb_locSrc': 'default',
        'x-channel': 'web',
        '_bb_loid': 'j:null',
        '_bb_bhid': '',
        '_bb_nhid': '1723',
        '_bb_vid': 'MTI2ODYyMTUxNzA=',
        '_bb_dsevid': '',
        '_bb_dsid': '',
        'csrftoken': 'cM7wdef2quyarEFKOw0qSRECQipTbVStmfwxkBtDx3u6RVB8p4lAG7AsmkiYi96Z',
        '_bb_home_cache': '316301a9.1.visitor',
        '_bb_bb2.0': '1',
        '_is_bb1.0_supported': '0',
        'is_integrated_sa': '0',
        'bb2_enabled': 'true',
        'ufi': '1',
        '_gcl_au': '1.1.657389654.1721282091',
        'bigbasket.com': 'e5f2b725-ba5d-4706-963e-4c265b2ce330',
        'adb': '0',
        '_gid': 'GA1.2.95321730.1721282092',
        'jarvis-id': 'e4de9fdc-340f-49dd-9303-9fa6c8f5f71f',
        '_fbp': 'fb.1.1721282092327.11535137222352572',
        'is_global': '0',
        '_bb_cid': '6',
        '_bb_sa_ids': '10204',
        '_bb_lat_long': lat_long_cookie,
        '_bb_aid': '"Mjk3NDM4MDYyOQ=="',
        '_bb_addressinfo': 'MTIuOTM2OTgwM3w4MC4xNzQwMjAyfE1hbGxpZ2EgTmFnYXJ8NjAwMTE3fENoZW5uYWl8MXxmYWxzZXx0cnVlfHRydWV8QmlnYmFza2V0ZWVy',
        '_bb_pin_code': pincode,
        '_bb_cda_sa_info': 'djEuY2RhX3NhLjYwMDExNy4xMDAuMTAyMDQ=',
        'csurftoken': 'ePVmMw.MTI2ODYyMTUxNzA=.1721285902977.6HfTZI+3UhGq9iGYq8deFMM+vOxof/XqvE9Gfn13YBc=',
        'ts': '2024-07-18%2012:34:44.083',
        '_is_tobacco_enabled': '0',
        '_gat_UA-27455376-1': '1',
        '_ga': 'GA1.1.1032771252.1721282092',
        'fs_uid': '#11EGJ5#5929047887261696:1083336064311850087:::#/1752818106',
        '_ga_FRRYG5VKHX': 'GS1.1.1721282091.1.1.1721286302.35.0.0',
    }

    headers = {
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9',
        'cache-control': 'no-cache',
        'content-type': 'application/json',
        'newrelic': 'eyJ2IjpbMCwxXSwiZCI6eyJ0eSI6IkJyb3dzZXIiLCJhYyI6IjgzNzMwNCIsImFwIjoiMTgzNDk4NzAwMiIsImlkIjoiYTk0NDNjY2YxZDI1YmIyZCIsInRyIjoiMTVmNGIzMzc3MTBhY2M4N2U2NWIyMjdhYmJlN2Y5ZGMiLCJ0aSI6MTcyMTI4NjMwMzk3OH19',
        'pragma': 'no-cache',
        'priority': 'u=1, i',
        'referer': 'https://www.bigbasket.com/ps/?q=tea&nc=as',
        'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'traceparent': '00-15f4b337710acc87e65b227abbe7f9dc-a9443ccf1d25bb2d-d25bb2d-01',
        'tracestate': '837304@nr=0-1-837304-1834987002-a9443ccf1d25bb2d----1721286303978',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
        'x-channel': 'BB-WEB',
        'x-tracker': 'fbb2bfd0-4840-4a8a-b8d1-b6206f82fa7a',
    }

    params = {
        'type': 'ps',
        'slug': 'tea',
        'page': '1',
        'bucket_id': '52',
    }

    response = requests.get(url, params=params, cookies=cookies, headers=headers)

    if response.status_code == 200:
        data = response.json()

        tabs = data.get('tabs', [])

        for tab in tabs:
            products_info = tab.get('product_info', {})
            products = products_info.get('products', [])

            for product in products:
                name = product.get('desc')
                pricing = product.get('pricing', {})
                mrp = pricing.get('discount', {}).get('mrp')
                images = product.get('images', [])
                if images:
                    image_url = images[0].get('s')  # Getting the small image URL
                else:
                    image_url = None
                product_url = f"https://www.bigbasket.com{product.get('absolute_url')}"
                ratings = product.get('avg_rating', 'Not available')
                ratings_count = product.get('rating_count', 'Not available')
                print(f"Product Name: {name}, Price: {mrp}, Image URL: {image_url}, Ratings: {ratings}, Ratings Count: {ratings_count}, Product URL: {product_url}")
    else:
        print(f"Failed to retrieve data. Status code: {response.status_code}")
        print(response.text)

# Prompt the user to input pincode and _bb_lat_long cookie
pincode = input("Enter the pincode: ")
lat_long_cookie = input("Enter the _bb_lat_long cookie value: ")

# Call the function with user inputs
fetch_product_details(pincode, lat_long_cookie)





