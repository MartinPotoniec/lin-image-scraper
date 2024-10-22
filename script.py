import os
import time
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import mimetypes

def fetch_page_content(url):
    response = requests.get(url)
    response.raise_for_status() 
    return response.text

def get_h1_text(soup):
    h1_tag = soup.find('h1')
    h1_text = h1_tag.get_text() if h1_tag else "no_h1"
    return h1_text.strip().replace(' ', '_').replace('/', '_').replace('\\', '_')

def download_image(img_url, img_filename):
    img_data = requests.get(img_url).content
    with open(img_filename, 'wb') as handler:
        handler.write(img_data)
    print(f"Downloaded {img_filename}")

def find_and_download_images(div_content, url, h1_text, output_dir):
    images = div_content.find_all('img')
    if not images:
        print("No images found in the 'toc-content' div.")
        return

    os.makedirs(output_dir, exist_ok=True) 

    for idx, img in enumerate(images, 1):
        img_url = img.get('src')
        if not img_url.startswith('http'):
            img_url = f'{url}/{img_url}'

        content_type = requests.head(img_url).headers.get('content-type')
        extension = mimetypes.guess_extension(content_type) or '.jpg'
        img_filename = os.path.join(output_dir, f'{h1_text}_image_{idx}{extension}')
        download_image(img_url, img_filename)

def scrape_toc_content(url):
    page_content = fetch_page_content(url)
    soup = BeautifulSoup(page_content, 'html.parser')

    h1_text = get_h1_text(soup)
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    output_dir = os.path.join("images", f"{h1_text}_{timestamp}")

    div_content = soup.find('div', class_='toc-content')
    if div_content:
        print(f"Scraping content from: {url}")
        find_and_download_images(div_content, url, h1_text, output_dir)
    else:
        print("No <div> with class 'toc-content' found.")

if __name__ == '__main__':
    import sys

    if len(sys.argv) != 2:
        print("Usage: python3 script.py <URL>")
        sys.exit(1)

    url = sys.argv[1]
    scrape_toc_content(url)
