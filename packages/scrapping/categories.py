from urllib.parse import urljoin
from .soup import get_soup


def get_categories(site_home_url):
    """
    GET all category URLs from the site homepage
    """
    soup = get_soup(site_home_url)

    nav_elements = soup.find('ul', {'class': 'nav-list'}).find('ul').find_all('a')

    categories = {}

    for nav_element in nav_elements:

        categorie_name = nav_element.text
        categorie_url = urljoin(site_home_url, nav_element.get('href'))

        categories[categorie_name.strip()] = categorie_url

    return categories


if __name__ == "__main__":
    site_home_url = "http://books.toscrape.com/index.html"
    print(get_categories(site_home_url))
