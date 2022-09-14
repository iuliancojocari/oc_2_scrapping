from urllib.parse import urljoin
from .soup import get_soup


def get_category_pages(cat_url):
    """
    Create and return a list with the category pages (links)
    """
    pages = [cat_url]

    while True:
        soup = get_soup(cat_url)

        cat_url = get_next_page_url(soup, cat_url)

        if not cat_url:
            break

        pages.append(cat_url)

    return pages


def get_next_page_url(soup, cat_url):
    """
    GET the next page url of a category
    """
    next_page_element = soup.select_one("li.next > a")

    if next_page_element is not None:
        next_page_url = next_page_element.get("href")
        page_url = urljoin(cat_url, next_page_url)

        return page_url
    else:
        return
