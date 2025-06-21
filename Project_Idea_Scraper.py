# pip install bs4 requests pandas html5lib
from bs4 import BeautifulSoup
import requests
import pandas as pd

# User-Agent header
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36"
}

all_scraped_data = []

def scrape_page_data():
    url = input("Enter URL :  ")
    tags_list = input("Enter Tags (space-separated): ").split()

    try:
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status() # Raise exception for HTTP errors (4xx or 5xx)
        print(f"Status Code: {response.status_code}")

        soup = BeautifulSoup(response.text, features="html5lib")

        return [item.get_text(strip=True) for item in soup.find_all(tags_list)]

    except requests.exceptions.RequestException as e:   # base exception class for ALL errors that can occur with the requests library
        print(f"Request failed for URL {url}: {e}") # here it shows which error it is (HTTPError, ConnectionError, Timeout)

        # If the server sent any response (even an error or anti-bot page 'captcha'), print its content for debugging.
        # print a snippet to help figure out why we were blocked.
        if hasattr(e, 'response') and e.response is not None:
            print("Response content snippet (check for anti-bot pages):\n", e.response.text[:500])
        return [] # Return empty list on failure

pages_to_scrape = int(input("How many pages you want to scrap :  "))
for _ in range(pages_to_scrape):
    page_data = scrape_page_data()
    all_scraped_data.extend(page_data) # Add data from the current page to the master list

print("\n--- All Scraped Data ---")
print(all_scraped_data)



# --- EXPORT TO EXCEL ---

df = pd.DataFrame(all_scraped_data)
df.columns = range(df.shape[1]) # Automatically set column names to 0, 1, 2, ...
OUTPUT_EXCEL_FILENAME = 'scraped_data.xlsx'

# index=False prevents Pandas from writing the DataFrame's index as a column in Excel.
df.to_excel(OUTPUT_EXCEL_FILENAME, index=False)

print(f"\nData successfully exported to '{OUTPUT_EXCEL_FILENAME}'!")



