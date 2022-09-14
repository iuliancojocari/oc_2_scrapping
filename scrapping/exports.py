import requests
from urllib.parse import urljoin


def download_book_img(img_file_name, book_url, image_url):
    """
    Download books images
    """
    with open(img_file_name + ".jpg", "wb") as handler:
        image_complete_url = urljoin(book_url, image_url)
        response = requests.get(image_complete_url)
        handler.write(response.content)
