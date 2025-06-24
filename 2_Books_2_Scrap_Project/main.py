import requests
from bs4 import BeautifulSoup


class BookScraper:
    def __init__(self, url):
        self.url = url
        self.page_data = None
        self.soup = None

    def fetch_data(self):
        response = requests.get(self.url)
        response.encoding = 'utf-8'  # Fix £ symbol
        if response.status_code == 200:
            print("✅ Web Site Accessible")
            self.page_data = response.text
            return True
        else:
            print("❌ Web Site Not Accessible")
            return False

    def parse_html(self):
        self.soup = BeautifulSoup(self.page_data, "lxml")

    def extract_books(self):
        books = []
        class_name = 'col-xs-6 col-sm-4 col-md-3 col-lg-3'
        fetched_books = self.soup.find_all('li', class_=class_name)

        for book in fetched_books:
            title = book.h3.a['title']
            price = book.find('p', class_='price_color').text

            books.append({
                'title': title,
                'price': price
            })
        return books

    def display_books(self, books):
        for book in books:
            print(f"📚 Title  : {book['title']}")
            print(f"💲 Price  : {book['price']}")
            print("-" * 40)


def main():
    url = "https://books.toscrape.com/"
    scraper = BookScraper(url)

    if scraper.fetch_data():
        scraper.parse_html()
        books = scraper.extract_books()
        scraper.display_books(books)


if __name__ == "__main__":
    main()
