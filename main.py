from msilib.schema import Directory
from ntpath import join
import requests
from bs4 import BeautifulSoup
import csv
from urllib.parse import urljoin
import os


url = "http://books.toscrape.com/index.html"

# Récupérer le contenu de la page principale
def get_soup(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    return soup

def get_caetegories(url):
    soup = get_soup(url)
    nav_elements = soup.find('ul', {'class':'nav-list'}).find('ul').find_all('a')

    categories = {}

    for nav_element in nav_elements:
        
        categorie_name = nav_element.text
        categorie_url = urljoin(url, nav_element.get('href'))
        
        categories[categorie_name.strip()] = categorie_url

    return categories

# Récupérer le lien vers la page suivante
def get_next_page_url(soup):
    next_page_element = soup.select_one('li.next > a')

    if next_page_element is not None:
        next_page_url = next_page_element.get('href')
        page_url = urljoin(url, next_page_url)
        
        return page_url
    else:
        return


# Liste contenant l'ensemble des liens des pages de la catégorie
def get_category_pages(url):
    pages = [url]

    while True:
        soup=get_soup(url)

        url = get_next_page_url(soup)

        if not url:
            break
        
        pages.append(url)

    return pages


def get_books_urls(url):
    pages = get_category_pages(url)
    #print(pages)
    book_urls = []

    for page in pages:
        soup = get_soup(page)

        articles = soup.find_all('article')

        for article in articles:
            book_url = article.select_one('h3 > a').get('href')
            book_urls.append(urljoin(url, book_url))

    return book_urls
        
def get_book_data(url):
    categories = get_caetegories(url)

    for cat_name, cat_url in categories.items():

        category_pages = get_category_pages(cat_url)
        print(category_pages)
        for category_page in category_pages:

            books = get_books_urls(category_page)

            directory = "data"
            if not os.path.exists(directory):
                os.makedirs(directory)

            filename = 'data/' + cat_name + '.csv'

            with open(filename, 'a', newline='', encoding='utf-8') as csvfile:

                fieldnames = ['product_page_url', 
                                        'title', 
                                        'category', 
                                        'product_description', 
                                        'image_url', 
                                        'universal_product_code', 
                                        'price_including_tax',
                                        'number_available',
                                        'review_rating']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

                if os.stat(filename).st_size == 0:
                    writer.writeheader()

                for book in books:
                        soup = get_soup(book)

                        product_page_url        = book
                        title                   = soup.h1.text
                        category                = soup.find('ul', {'class':'breadcrumb'}).select('li')[2].find('a').text
                        try:
                            product_description     = soup.find(id='product_description').find_next_sibling('p').text
                        except:
                            product_description = 'N/A'
                        image_url               = soup.find('div', {'class' : 'item'}).find('img').get('src')
                        universal_product_code  = soup.find('table', {'class': 'table'}).select('td')[0].text
                        price_including_tax     = soup.find('table', {'class': 'table'}).select('td')[2].text
                        number_available        = soup.find('table', {'class': 'table'}).select('td')[5].text
                        review_rating           = soup.find('table', {'class': 'table'}).select('td')[6].text

                            
                        writer.writerow({   'product_page_url'          : product_page_url, 
                                            'title'                     : title,
                                            'category'                  : category,
                                            'product_description'       : product_description,
                                            'image_url'                 : image_url,
                                            'universal_product_code'    : universal_product_code,
                                            'price_including_tax'       : price_including_tax,
                                            'number_available'          : number_available,
                                            'review_rating'             : review_rating
                                            })


get_book_data(url)