# imports
import requests
from bs4 import BeautifulSoup

WEB_URL = "https://pk.khaadi.com/new-in/"
HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

def fetch_url_data(url):
    response = requests.get(url, headers=HEADERS)
    response.encoding = 'utf-8'
    return response

def check_status(response):
    return response.status_code == 200

def parse_html(box):
    try:
        title = box.find("h2", class_="pdp-link-heading").get_text(strip=True)
        price = box.find("span", class_="value cc-price").get_text(strip=True)
        category = box.find("div", class_="product-brand").get_text(strip=True)
        # image = box.find("img", class_="tile-image")["src"]
        image_container = box.find("div", class_="image-container")
        # image = image_container.get("data-large-0") 
        # image = image_container.get("data-large-0", "").replace(" ", "")
        # image = image_container.get("data-large-0", "").strip().replace(" ", "").replace("\n", "")
        image = image_container.get("data-large-0", "")
        image = image.replace(" ", "").replace("\n", "").strip()

        link = "https://pk.khaadi.com" + box.find("a", class_="plpRedirectPdp")["href"]
        
        return {
            "title": title,
            "price": price,
            "category": category,
            "image": image,
            "link": link
        }
    except AttributeError:
        return None

def find_clothing_items(soup):
    all_products = []
    product_tiles = soup.find_all("div", class_="product-tile")

    for tile in product_tiles:
        data = parse_html(tile)
        if data:
            all_products.append(data)
    return all_products

def prepare_soup(response_text):
    soup = BeautifulSoup(response_text, "lxml")
    data = find_clothing_items(soup)
    display_results(data)
    return data

def Web_Scraper(url):
    response = fetch_url_data(url)
    if check_status(response):
        prepare_soup(response.text)
    else:
        print("❌ Failed to access website.")

def display_results(data_list):
    for i, item in enumerate(data_list, start=1):
        print(f"\n🧥 Product {i}")
        print(f"👗 Title   : {item['title']}")
        print(f"💰 Price   : {item['price']}")
        print(f"📂 Category: {item['category']}")
        print(f"🖼️ Image   : {item['image']}")
        print(f"🔗 Link    : {item['link']}")
        print("-" * 60)

def main():
    Web_Scraper(WEB_URL)

if __name__ == "__main__":
    main()


