import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

WEB_URL = "https://books.toscrape.com/"

def get_url_data(url):
    response = requests.get(url)
    response.encoding = 'utf-8'
    return response

def check_status(response):
    if response.status_code == 200:
        return True
    else:
        print(f"❌ Failed to access: {response.url}")
        return False

def get_books(soup):
    class_name = 'col-xs-6 col-sm-4 col-md-3 col-lg-3'
    return soup.find_all('li', class_=class_name)

def parse_book(book):
    title = book.h3.a['title']
    price = book.find('p', class_='price_color').text.strip()
    availability = book.find('p', class_='instock availability').text.strip()
    return {
        'title': title,
        'price': price,
        'availability': availability
    }

def print_book(book):
    print(f" 📚 Title       : {book['title']}")
    print(f" 💲 Price       : {book['price']}")
    if book['availability'].lower() == 'in stock':
        print(f" ✅ Availability: {book['availability']}")
    else:
        print(f" ❌ Availability: {book['availability']}")
    print("-" * 40)

def has_next_page(soup, current_url):
    next_li = soup.find('li', class_='next')
    if next_li:
        next_href = next_li.a['href']
        return urljoin(current_url, next_href)
    return None

def main():
    current_url = WEB_URL
    page = 1

    while True:
        print(f"\n🔁 Scraping Page {page}: {current_url}")
        response = get_url_data(current_url)

        if not check_status(response):
            break

        soup = BeautifulSoup(response.text, 'lxml')
        books = get_books(soup)

        for book_html in books:
            book_data = parse_book(book_html)
            print_book(book_data)

        next_url = has_next_page(soup, current_url)
        if next_url:
            current_url = next_url
            page += 1
        else:
            print("\n✅ All pages scraped!")
            break

if __name__ == "__main__":
    main()
