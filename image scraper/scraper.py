import requests
from bs4 import BeautifulSoup
import os
import urllib.parse
import time
import random

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

def fetch_image_urls(search_query, num_images=5):
    query = urllib.parse.quote_plus(search_query)
    url = f"https://www.bing.com/images/search?q={query}&form=HDRSC2&first=1&tsc=ImageBasicHover"

    response = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(response.text, "html.parser")

    image_elements = soup.find_all("a", {"class": "iusc"}, limit=num_images)
    image_urls = []

    for elem in image_elements:
        try:
            m_json = eval(elem.get("m"))  # be cautious; Bing stores metadata in `m` as a dict-string
            murl = m_json.get("murl")
            if murl:
                image_urls.append(murl)
        except Exception as e:
            print("Error parsing image element:", e)

    return image_urls

def download_images(image_urls, download_dir="images", prefix="img"):
    os.makedirs(download_dir, exist_ok=True)
    
    for idx, img_url in enumerate(image_urls):
        try:
            img_data = requests.get(img_url, headers=HEADERS).content
            filename = os.path.join(download_dir, f"{prefix}_{idx}.jpg")
            with open(filename, "wb") as f:
                f.write(img_data)
            print(f"Downloaded {filename}")
        except Exception as e:
            print(f"Failed to download {img_url}: {e}")

        time.sleep(random.uniform(1, 2))  # polite delay

# Example usage
if __name__ == "__main__":
    medical_id = "CT scan lung cancer"  # Replace with real ID/description
    images = fetch_image_urls(medical_id, num_images=3)
    download_images(images, prefix=medical_id.replace(" ", "_"))
