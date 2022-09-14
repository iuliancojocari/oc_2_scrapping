import csv
import os
import re
from urllib.parse import urljoin
from scrapping.soup import get_soup
from scrapping.categories import get_categories
from scrapping.books import get_book_urls
from scrapping.exports import download_book_img
from scrapping.utils import create_directory
from scrapping.constants import URL


def book_info(book_url):
    """
    GET all requested info about a book
    """
    soup = get_soup(book_url)

    product_description = soup.select_one("#product_description + p")

    data = {
        "product_page_url": book_url,
        "title": soup.h1.text,
        "category": soup.find("ul", {"class": "breadcrumb"})
        .select("li")[2]
        .find("a")
        .string,
        "product_description": product_description.text
        if product_description
        else "N/A",
        "image_url": urljoin(
            book_url, soup.find("div", {"class": "item"}).find("img").get("src")
        ),
        "universal_product_code": soup.find("table", {"class": "table"})
        .select("td")[0]
        .string,
        "price_including_tax": soup.find("table", {"class": "table"})
        .select("td")[2]
        .string,
        "number_available": soup.find("table", {"class": "table"})
        .select("td")[5]
        .string,
        "review_rating": soup.find("table", {"class": "table"}).select("td")[6].string,
    }

    return data


def get_book_data(site_home_url):
    """
    This is the main function
    The function will fetch all the requested information
    of all the books, for each of the categories,
    from the site http://books.toscrape.com/index.html
    """
    categories = get_categories(site_home_url)

    for cat_name, cat_url in categories.items():
        print("\n")
        print("**********************************************")
        print("         Category Name - " + cat_name + "     ")
        print("**********************************************")

        # GET the list of books; of all pages in the category
        book_urls = get_book_urls(cat_url)

        # Create data folder; a forlder by category is also created
        cat_directory = "data/" + cat_name.lower() + "/"
        create_directory(cat_directory)

        filename = cat_directory + cat_name.lower() + ".csv"

        with open(filename, "a", encoding="utf-8", newline="") as csvfile:
            fieldnames = [
                "product_page_url",
                "title",
                "category",
                "product_description",
                "image_url",
                "universal_product_code",
                "price_including_tax",
                "number_available",
                "review_rating",
            ]

            writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=";")

            # Check if the .csv file is empty and write header
            if os.stat(filename).st_size == 0:
                writer.writeheader()

            for book_url in book_urls:
                book = book_info(book_url)

                print("Book Name - " + book["title"])

                writer.writerow(
                    {
                        "product_page_url": book["product_page_url"],
                        "title": book["title"],
                        "category": book["category"],
                        "product_description": book["product_description"],
                        "image_url": book["image_url"],
                        "universal_product_code": book["universal_product_code"],
                        "price_including_tax": book["price_including_tax"],
                        "number_available": book["number_available"],
                        "review_rating": book["review_rating"],
                    }
                )

                # Download images
                # the images are stored into img folder into category folder
                img_directory = cat_directory + "/img/"
                create_directory(img_directory)

                # replace spaces by underscore in the images name
                img_file_name = book["title"].replace(" ", "_")
                # remove all special character from the image name
                img_file_name = img_directory + re.sub(
                    r"[^a-zA-Z0-9_]", "", img_file_name
                )

                download_book_img(img_file_name, book_url, book["image_url"])


if __name__ == "__main__":
    get_book_data(URL)
