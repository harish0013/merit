import requests
from bs4 import BeautifulSoup
import pandas as pd

# Function to scrape Wikipedia page content
def scrape_wikipedia(url):
    response = requests.get(url)
    if response.status_code == 200:
        print(f"Successfully fetched the webpage: {url}")
        soup = BeautifulSoup(response.content, "html.parser")
        # Example: Scraping page title
        title = soup.find("div", class_="fn").text.strip()
        # Example: Scraping page content
        content = soup.find("table", class_="infobox vcard").get_text()
        return {"Title": title, "Content": content}
    else:
        print(f"Failed to fetch the webpage: {url}")
        return None

# Example usage: Scraping a specific Wikipedia page
wiki_url = "https://en.wikipedia.org/wiki/Suresh_Raina"
data = scrape_wikipedia(wiki_url)
if data:
    print(data["Title"])
    print(data["Content"][:500])  # Print first 500 characters of content

    # # Save to CSV file
    # df = pd.DataFrame([data])
    # df.to_csv("Python_Programming_Language_Wikipedia.csv", index=False)
    # print("Data has been saved to Python_Programming_Language_Wikipedia.csv")
    #
