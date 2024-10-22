import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
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

    images = images[:-2] if len(images) > 2 else images

    idx = 1
    for img in images:
        img_url = img.get('src')
        if not img_url.startswith('http'):
            img_url = urljoin(url, img_url)

        if img_url.endswith('.svg'):
            print(f"Skipping SVG image: {img_url}")
            continue

        content_type = requests.head(img_url).headers.get('content-type')
        if 'svg' in content_type:
            print(f"Skipping SVG image: {img_url}")
            continue

        extension = mimetypes.guess_extension(content_type) or '.jpg'
        img_filename = os.path.join(output_dir, f'{h1_text}_image_{idx}{extension}')
        download_image(img_url, img_filename)
        idx += 1

def download_main_image(soup, url, h1_text, output_dir):
    main_image_div = soup.find('div', class_="w-full border-2 border-heading rounded-[20px] md:rounded-[40px] m-0 overflow-hidden min-h-[200px] md:min-h-[350px] lg:min-h-[500px]")
    
    if main_image_div:
        img_tag = main_image_div.find('img')
        if img_tag:
            img_url = img_tag.get('src')
            full_img_url = urljoin(url, img_url)

            if full_img_url.endswith('.svg'):
                print(f"Skipping SVG image: {full_img_url}")
                return

            img_filename = os.path.join(output_dir, f'{h1_text}_image_main{os.path.splitext(full_img_url)[1]}')
            
            try:
                download_image(full_img_url, img_filename)
            except Exception as e:
                print(f"Failed to download main image: {e}")
        else:
            print("No <img> tag found inside the main image div.")
    else:
        print("No main image div found on the page.")

def scrape_toc_content(url):
    page_content = fetch_page_content(url)
    soup = BeautifulSoup(page_content, 'html.parser')

    h1_text = get_h1_text(soup)
    output_dir = os.path.join("images", f"{h1_text}")

    os.makedirs(output_dir, exist_ok=True)

    download_main_image(soup, url, h1_text, output_dir)

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
