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

