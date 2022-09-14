import requests
from bs4 import BeautifulSoup


def get_soup(url):
    """
    GET HTML content from a web page
    """
    response = requests.get(url)
    soup = response.content
    soup = BeautifulSoup(soup, 'html.parser')

    return soup


if __name__ == "__main__":
    url = "http://books.toscrape.com/index.html"
    print(get_soup(url))
