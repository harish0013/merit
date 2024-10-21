import requests
import json
import csv
from bs4 import BeautifulSoup


# Define the URL for the POST request and job detail pages
url = "https://www.jobs.abbott/widgets"
base_job_url = "https://www.jobs.abbott/us/en/job/"

# Headers for the request
headers = {
    'Content-Type': 'application/json'
}


# Function to scrape one page of results
def scrape_page(offset=0):
    # Define the payload for the POST request
    payload = {
        "lang": "en_us",
        "deviceType": "desktop",
        "country": "us",
        "pageName": "search-results",
        "ddoKey": "refineSearch",
        "sortBy": "",
        "subsearch": "",
        "from": offset,  # Pagination offset
        "jobs": True,
        "counts": True,
        "all_fields": [
            "category",
            "type",
            "country",
            "state",
            "city",
            "division"
        ],
        "size": 10,  # Number of results per page
        "clearAll": True,
        "jdsource": "facets",
        "isSliderEnable": False,
        "pageId": "page17",
        "siteType": "external",
        "location": "",
        "keywords": "",
        "global": True,
        "selected_fields": {},
        "locationData": {}
    }

    # Send the POST request
    response = requests.post(url, headers=headers, json=payload)

    # Check if the request was successful
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to retrieve data from page offset {offset}. Status code: {response.status_code}")
        return None


# Function to scrape job details from the job detail page


job_id_lst = []


# Main function to scrape all pages and collect job details
def scrape_all_jobs(total_hits):
    all_jobs = []
    page_size = 10  # Number of jobs per page
    total_pages = total_hits // page_size + (total_hits % page_size > 0)

    for page in range(total_pages):
        offset = page * page_size
        print(f"Scraping page {page + 1}/{total_pages} (offset: {offset})")
        data = scrape_page(offset)

        if data and "refineSearch" in data and "data" in data["refineSearch"]:
            jobs = data['refineSearch']['data']['jobs']
            for job in jobs:
                job_id = job.get('jobId')
                # print(f"Scraping job ID: {job_id}")

                job_id_lst.append(job_id)

        else:
            print(f"No data found on page {page + 1}")
    return


# Define the number of total hits (total number of job postings)
total_hits = 2500  # This should be dynamically obtained from the first response
print(f"Total hits: {total_hits}")

# Scrape all pages and collect job details
scrape_all_jobs(total_hits)

import requests, json, re
from bs4 import BeautifulSoup
import html, os
import pandas as pd

csv_file = "Abbort_Career_21Oct2024.csv"
file_exists = os.path.isfile(csv_file)

cookies = {
    's_fid': '0821E04D9919F5B8-2C8E9A4169CEF2B9',
    's_cc': 'true',
    '_gcl_au': '1.1.1816205325.1728291093',
    'code_ver': '2.22.0',
    '_gid': 'GA1.2.1759715831.1728291094',
    'rally-visitor-tracking-id': 'v-1728291094116',
    '_hjSessionUser_750829': 'eyJpZCI6IjBhNGMxMWI5LThjMTAtNTJlMS05NzNiLTZlZmZlZWJkM2Q0NCIsImNyZWF0ZWQiOjE3MjgyOTEwOTQwMTgsImV4aXN0aW5nIjp0cnVlfQ==',
    '_ccid': '1728291512366ddky1o5wl',
    '_ga_YBJ9ZJWL92': 'deleted',
    '_ga_YBJ9ZJWL92': 'deleted',
    'PLAY_SESSION': 'eyJhbGciOiJIUzI1NiJ9.eyJkYXRhIjp7IkpTRVNTSU9OSUQiOiJhNTEyMTZlNC1mYmEzLTRiOGYtODBlYS0xNDJjOTg5YjgzOGIifSwibmJmIjoxNzI4MzU2NjQxLCJpYXQiOjE3MjgzNTY2NDF9.uZYu_hmVE7PbxzIlKgkxjo5hgTukGRVXHirGZ1gU04M',
    'PHPPPE_ACT': 'a51216e4-fba3-4b8f-80ea-142c989b838b',
    '_hjSession_750829': 'eyJpZCI6IjI3NDlmZWVjLTcwMDktNGZiYi05NThkLThkOTc3NjkwMzgxZiIsImMiOjE3MjgzNTY2NDM2MTgsInMiOjAsInIiOjAsInNiIjowLCJzciI6MCwic2UiOjAsImZzIjowLCJzcCI6MH0=',
    'ermgfd_TAsessionID': 'e23ce9dd-3cf7-4066-b4d4-5f907b3589e8|NEW',
    'rally-previous-page-url': 'https%3A%2F%2Fwww.jobs.abbott%2Fearly-careers%3Futm_content%3Dcareers-students%26utm_campaign%3D.com-CTAs%26utm_medium%3Dwebsite%26utm_source%3Dabbott.co.uk',
    'rally-event-click': '',
    'utm_content': 'careers-students',
    's_sq': '%5B%5BB%5D%5D',
    's_nr': '1728356672220-Repeat',
    '_ga_YBJ9ZJWL92': 'GS1.1.1728356643.3.1.1728356672.0.0.0',
    '_ga': 'GA1.2.1194676364.1728291094',
    'ermgfd_notice_behavior': 'implied|as',
}

headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'en-US,en;q=0.9',
    'cache-control': 'max-age=0',
    # 'cookie': 's_fid=0821E04D9919F5B8-2C8E9A4169CEF2B9; s_cc=true; _gcl_au=1.1.1816205325.1728291093; code_ver=2.22.0; _gid=GA1.2.1759715831.1728291094; rally-visitor-tracking-id=v-1728291094116; _hjSessionUser_750829=eyJpZCI6IjBhNGMxMWI5LThjMTAtNTJlMS05NzNiLTZlZmZlZWJkM2Q0NCIsImNyZWF0ZWQiOjE3MjgyOTEwOTQwMTgsImV4aXN0aW5nIjp0cnVlfQ==; _ccid=1728291512366ddky1o5wl; _ga_YBJ9ZJWL92=deleted; _ga_YBJ9ZJWL92=deleted; PLAY_SESSION=eyJhbGciOiJIUzI1NiJ9.eyJkYXRhIjp7IkpTRVNTSU9OSUQiOiJhNTEyMTZlNC1mYmEzLTRiOGYtODBlYS0xNDJjOTg5YjgzOGIifSwibmJmIjoxNzI4MzU2NjQxLCJpYXQiOjE3MjgzNTY2NDF9.uZYu_hmVE7PbxzIlKgkxjo5hgTukGRVXHirGZ1gU04M; PHPPPE_ACT=a51216e4-fba3-4b8f-80ea-142c989b838b; _hjSession_750829=eyJpZCI6IjI3NDlmZWVjLTcwMDktNGZiYi05NThkLThkOTc3NjkwMzgxZiIsImMiOjE3MjgzNTY2NDM2MTgsInMiOjAsInIiOjAsInNiIjowLCJzciI6MCwic2UiOjAsImZzIjowLCJzcCI6MH0=; ermgfd_TAsessionID=e23ce9dd-3cf7-4066-b4d4-5f907b3589e8|NEW; rally-previous-page-url=https%3A%2F%2Fwww.jobs.abbott%2Fearly-careers%3Futm_content%3Dcareers-students%26utm_campaign%3D.com-CTAs%26utm_medium%3Dwebsite%26utm_source%3Dabbott.co.uk; rally-event-click=; utm_content=careers-students; s_sq=%5B%5BB%5D%5D; s_nr=1728356672220-Repeat; _ga_YBJ9ZJWL92=GS1.1.1728356643.3.1.1728356672.0.0.0; _ga=GA1.2.1194676364.1728291094; ermgfd_notice_behavior=implied|as',
    'priority': 'u=0, i',
    'sec-ch-ua': '"Google Chrome";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'none',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36',
}
all_jobs = []
for job_id in job_id_lst:
    try:
        job_url = "https://www.jobs.abbott/us/en/job/" + job_id
        response = requests.get(job_url, headers=headers).content
        response = BeautifulSoup(response)
        for val in response.select("script"):
            if "widgetApiEndpoint" in val.text:
                data = val.text
                break
        data = data[data.find("phApp.ddo ="):].replace("phApp.ddo =", "")
        data = data[:data.find("; phApp.experimentData = {")]
        data = json.loads(data.replace("/*&lt;!--*/ var phApp = phApp || ", "").replace('; /*--&gt;*/', ''))
        print(data)
        main_data = data.get("jobDetail", {}).get("data", {}).get("job", {})
        if main_data:
            out_dict = {}
            extract_data = main_data.get("structureData", {})
            out_dict["id"] = main_data.get("jobId", "")
            out_dict["corporate_title"] = main_data.get("title", "")
            out_dict["job_title"] = main_data.get("ml_title", "")
            out_dict["job_function"] = main_data.get("occupationalCategory", "")
            out_dict["city"] = main_data.get("city", "")
            out_dict["state"] = main_data.get("state", "")
            out_dict["country"] = main_data.get("country", "")
            out_dict["division"] = main_data.get("division", "")
            out_dict["jobType"] = main_data.get("type", "")
            out_dict["skillset"] = main_data.get("ml_job_parser", {}).get("ml_skills", [])
            out_dict["currency"] = ""
            out_dict["applyActive"] = ""
            out_dict["job_application_url"] = main_data.get("applyUrl", "")
            out_dict["page_url"] = job_url
            out_dict["requirement_details"] = main_data.get("ml_job_parser", {}).get("requirement_sentences", "")
            out_dict["description"] = re.sub(r'<.*?>', '', html.unescape(main_data.get("description", ""))).replace(
                '\n', ' ').replace('\xa0', ' ')
            out_dict["job_code"] = main_data.get("jobCode", "")
            out_dict["job_travel"] = main_data.get("travel", "")
            out_dict["industry"] = main_data.get("industry", "")
            out_dict["sub_category"] = main_data.get("subCategory", "")
            out_dict["category"] = main_data.get("category_raw", "")
            out_dict["job_updated_date"] = main_data.get("jobUpdatedDate", "")
            out_dict["job_posted_date"] = extract_data.get("datePosted", "")
            out_dict["workHours"] = extract_data.get("workHours", "")
            out_dict["salaryRange"] = main_data.get("salaryRange", "")
            out_dict["is_remote"] = main_data.get("ml_job_parser", {}).get("is_remote", "")
            out_dict["experience_details"] = main_data.get("ml_job_parser", {}).get("experience_sentences", "")
            out_dict["educational_qualification"] = main_data.get("ml_job_parser", {}).get("good_to_have_education", "")
            out_dict["responsibilities"] = main_data.get("ml_job_parser", {}).get("responsibility_sentences", "")
            out_dict["significant_work_activities"] = main_data.get("significantWorkActivities", "")
            out_dict["medical_surveillance"] = main_data.get("productAlignment", "")
            out_dict["other_location"] = [val.get("location", "") for val in main_data.get("multi_location") if
                                          val.get("location", "")]
            print(job_id)
            # all_jobs.append(out_dict)
            df = pd.DataFrame([out_dict])

            # Write to CSV file, creating headers if the file does not exist
            df.to_csv(csv_file, mode='a', header=not file_exists, index=False)

            # Update file_exists to True after the first write
            file_exists = True
    except Exception as e:
        print(e)
        pass
        all_jobs.append(job_id)

# df = pd.DataFrame(all_jobs)

# Write the DataFrame to a CSV file
# df.to_csv('Abbort_Career_07Oct2024.csv', index=False)

# # Or, to write to an Excel file
# df.to_excel('job_data.xlsx', index=False)