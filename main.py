import requests
import csv
import os
import re
from urllib.parse import urljoin
from packages.scrapping.soup import get_soup
from packages.scrapping.categories import get_categories
from packages.scrapping.books import get_book_urls


url = "http://books.toscrape.com/index.html"

def create_directory(directory):
    """
    Create new directory
    """
    if not os.path.exists(directory):
        os.makedirs(directory)


def download_book_img(img_file_name, book_url, image_url):
    """
    Download books images
    """
    with open(img_file_name + '.jpg', 'wb') as handler:
        image_complete_url = urljoin(book_url, image_url)
        response = requests.get(image_complete_url)
        handler.write(response.content)


def get_book_data(site_home_url):
    categories = get_categories(site_home_url)

    for cat_name, cat_url in categories.items():
        print('\n')
        print('**********************************************')
        print('         Category Name - ' + cat_name + '     ')
        print('**********************************************')

        # GET the list of books; of all pages in the category
        book_urls = get_book_urls(cat_url)

        # Create data folder; a forlder by category is also created
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

            writer = csv.DictWriter(csvfile,
                                    fieldnames=fieldnames,
                                    delimiter=';')

            # Check if the .csv file is empty and write header
            if os.stat(filename).st_size == 0:
                writer.writeheader()

            for book_url in book_urls:
                soup = get_soup(book_url)

                # Scrapping book data
                product_page_url = book_url
                title = soup.h1.text
                category = soup.find('ul', {'class': 'breadcrumb'}).select('li')[2].find('a').string
                try:
                    product_description = soup.find(id='product_description').find_next_sibling('p').string
                except:
                    product_description = 'N/A'
                image_url = urljoin(book_url, soup.find('div', {'class': 'item'}).find('img').get('src'))
                universal_product_code = soup.find('table', {'class': 'table'}).select('td')[0].string
                price_including_tax = soup.find('table', {'class': 'table'}).select('td')[2].string
                number_available = soup.find('table', {'class': 'table'}).select('td')[5].string
                review_rating = soup.find('table', {'class': 'table'}).select('td')[6].string

                print('Book Name - ' + title)

                # Write data in the .csv file
                writer.writerow({'product_page_url': product_page_url,
                                 'title': title,
                                 'category': category,
                                 'product_description': product_description,
                                 'image_url': image_url,
                                 'universal_product_code': universal_product_code,
                                 'price_including_tax': price_including_tax,
                                 'number_available': number_available,
                                 'review_rating': review_rating})

                # Download images
                img_directory = cat_directory + '/img/'  # the images are stored into img folder into category folder
                create_directory(img_directory)  # create the img folder

                img_file_name = title.replace(' ', '_')  # replace spaces by underscore in the images name
                img_file_name = img_directory + re.sub(r"[^a-zA-Z0-9_]", "", img_file_name)  # remove all special character from the image name

                download_book_img(img_file_name, book_url, image_url)


if __name__ == "__main__":
    get_book_data(url)
