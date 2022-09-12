from dataclasses import replace
import requests
from bs4 import BeautifulSoup
import csv
from urllib.parse import urljoin
import os
import re

url = "http://books.toscrape.com/index.html"

# Récupérer le contenu de la page principale
def get_soup(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    return soup

def get_categories(site_home_url):
    soup = get_soup(site_home_url)
    nav_elements = soup.find('ul', {'class':'nav-list'}).find('ul').find_all('a')

    categories = {}

    for nav_element in nav_elements:
        
        categorie_name = nav_element.text
        categorie_url = urljoin(site_home_url, nav_element.get('href'))
        
        categories[categorie_name.strip()] = categorie_url

    return categories

# Récupérer le lien vers la page suivante
def get_next_page_url(soup, cat_url):
    next_page_element = soup.select_one('li.next > a')

    if next_page_element is not None:
        next_page_url = next_page_element.get('href')
        page_url = urljoin(cat_url, next_page_url)
        
        return page_url
    else:
        return


# Liste contenant l'ensemble des liens des pages de la catégorie
def get_category_pages(cat_url):
    pages = [cat_url]

    while True:
        soup=get_soup(cat_url)

        cat_url = get_next_page_url(soup, cat_url)

        if not cat_url:
            break
        
        pages.append(cat_url)

    return pages

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

def create_directory(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)
    
def download_cat_img(img_file, book, image_url):
    with open(img_file + '.jpg', 'wb') as handler:
        image_complete_url = urljoin(book, image_url)
        response = requests.get(image_complete_url)
        handler.write(response.content)
        
def get_book_data(site_home_url):
    categories = get_categories(site_home_url)
    
    print("Processing...")

    for cat_name, cat_url in categories.items():
        print('\n')
        print('**********************************************')
        print('         Category Name - ' + cat_name + '     ')
        print('**********************************************')

        books = get_book_urls(cat_url)
        
        cat_directory = "data/" + cat_name.lower() + "/"
        create_directory(cat_directory)

        filename = cat_directory + cat_name.lower() + '.csv'

        with open(filename, 'a', encoding='utf-8', newline='') as csvfile:

            fieldnames = ['product_page_url', 
                                    'title', 
                                    'category', 
                                    'product_description', 
                                    'image_url', 
                                    'universal_product_code', 
                                    'price_including_tax',
                                    'number_available',
                                    'review_rating']
                                    
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=';')

            if os.stat(filename).st_size == 0:
                writer.writeheader()

            for book in books:
                soup = get_soup(book)

                product_page_url        = book
                title                   = soup.h1.text
                category                = soup.find('ul', {'class':'breadcrumb'}).select('li')[2].find('a').text
                product_description     = soup.find(id='product_description').find_next_sibling('p').string
                image_url               = soup.find('div', {'class' : 'item'}).find('img').get('src')
                universal_product_code  = soup.find('table', {'class': 'table'}).select('td')[0].text
                price_including_tax     = soup.find('table', {'class': 'table'}).select('td')[2].text
                number_available        = soup.find('table', {'class': 'table'}).select('td')[5].text
                review_rating           = soup.find('table', {'class': 'table'}).select('td')[6].text

                print('Book Name - ' + title)


                writer.writerow({   'product_page_url'          : product_page_url, 
                                    'title'                     : title,
                                    'category'                  : category,
                                    'product_description'       : product_description.encode('utf-8'),
                                    'image_url'                 : image_url,
                                    'universal_product_code'    : universal_product_code,
                                    'price_including_tax'       : price_including_tax,
                                    'number_available'          : number_available,
                                    'review_rating'             : review_rating
                                    })


                img_directory = cat_directory + '/img/'
                create_directory(img_directory)

                img_file = title.replace(' ', '_')
                img_file = img_directory +  re.sub(r"[^a-zA-Z0-9_]","",img_file)

                download_cat_img(img_file, book, image_url)              


get_book_data(url)