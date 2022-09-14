from urllib.parse import urljoin
from .soup import get_soup
from .category_pages import get_category_pages


def get_book_urls(cat_url):
    pages = get_category_pages(cat_url)

    book_urls = []

    for page in pages:
        soup = get_soup(page)

        articles = soup.find_all('article')

        for article in articles:
            book_url = article.select_one('h3 > a').get('href')
            book_urls.append(urljoin(cat_url, book_url))

    return book_urls


if __name__ == "__main__":
    cat_url = "http://books.toscrape.com/catalogue/category/books/mystery_3/index.html"
    print(get_book_urls(cat_url))
