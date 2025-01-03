import requests
import json
from pathlib import Path

# Path to the JSON file containing scraped data
JSON_FILE_PATH = "scraped-data.json"
# API endpoint of your Next.js API route
API_URL = "https://chatbot.motionu.club/api/product"  # Replace with your actual API URL

def automate_data_entry():
    try:
        # Load data from JSON file
        json_file = Path(JSON_FILE_PATH)
        if not json_file.exists():
            print(f"JSON file not found: {JSON_FILE_PATH}")
            return

        with open(json_file, "r", encoding="utf-8") as f:
            data = json.load(f)

        # Iterate over each entry and send POST request
        for entry in data:
            if len(entry) >= 4:
                barcode = entry[0]  # First element is the barcode (serialNumber)
                product_name = entry[1]  # Second element is the product name (productName)
                reason = entry[2]  # Third element is the reason (reason)
                image_path = entry[3]  # Fourth element is the image path (imageUrl)

                # Prepare form data
                form_data = {
                    "productName": product_name,
                    "serialNumber": barcode,
                    "reason": reason,
                    "imageUrl": image_path  # Assuming imageUrl is the file path or a URL to the image
                }

                # Send POST request with the form data
                response = requests.post(API_URL, data=form_data)

                if response.status_code == 200:
                    print(f"Successfully added product: {product_name}")
                else:
                    print(f"Failed to add product: {product_name}")
                    print(f"Response: {response.status_code} - {response.text}")

            else:
                print(f"Invalid entry format: {entry}")

    except FileNotFoundError as e:
        print(f"File not found error: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    automate_data_entry()
