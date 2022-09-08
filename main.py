import requests
from bs4 import BeautifulSoup
import csv

url = 'http://books.toscrape.com/catalogue/sharp-objects_997/index.html'

response = requests.get(url)

if response.ok:
    soup = BeautifulSoup(response.text, 'lxml')

    product_page_url        = response.url
    title                   = soup.h1.text
    category                = soup.find('ul', {'class':'breadcrumb'}).select('li')[2].find('a').text
    product_description     = soup.find(id='product_description').find_next_sibling('p').text
    image_url               = soup.find('div', {'class' : 'item'}).find('img').get('src')
    universal_product_code  = soup.find('table', {'class': 'table'}).select('td')[0].text
    price_including_tax     = soup.find('table', {'class': 'table'}).select('td')[2].text
    number_available        = soup.find('table', {'class': 'table'}).select('td')[5].text
    review_rating           = soup.find('table', {'class': 'table'}).select('td')[6].text

    with open('list_books.csv', 'w', newline='', encoding='utf-8') as csvfile:
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

        writer.writeheader()
        writer.writerow({'product_page_url'             : product_page_url, 
                            'title'                     : title,
                            'category'                  : category,
                            'product_description'       : product_description,
                            'image_url'                 : image_url,
                            'universal_product_code'    : universal_product_code,
                            'price_including_tax'       : price_including_tax,
                            'number_available'          : number_available,
                            'review_rating'             : review_rating})
