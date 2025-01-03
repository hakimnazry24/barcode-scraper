import requests
from bs4 import BeautifulSoup
import json

def scrape_link(url, output_file, image_url, reason):
    try:
        
        response = requests.get(url)
        response.raise_for_status()

        # print(response.text)
        soup = BeautifulSoup(response.text, "html.parser")

        table = soup.find("table")

        if not table:
            print("No table found")
            return

        rows = table.find_all("tr")
        
        data = []

        for row in rows[1:]:
            cols = row.find_all("td")
            if len(cols) >= 3:  # Ensure at least three columns exist
                barcode = cols[1].get_text(strip=True)  # Second column
                product_name = cols[2].get_text(strip=True)  # Third column
                data.append([barcode, product_name, reason, image_url])

        print("Scraped Data:")
        for barcode, product_name, reason, image_url in data:
            print(f"Barcode: {barcode}, Product Name: {product_name}")

        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)


    except Exception as e:
        print(f"An error occured:{e}")


if __name__ == "__main__":
    output_file = "scraped-data.json"
    url = input("Enter the url to scrape: ")
    reason = input("Enter reason for the product get boycotted: ")
    imageUrl = input("Enter image URL: ")
    scrape_link(url, output_file, imageUrl, reason)