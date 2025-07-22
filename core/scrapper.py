import requests
from bs4 import BeautifulSoup
import json

URL = "https://www.amazon.in/gp/bestsellers/books"

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Accept-Language': 'en-US,en;q=0.5'
}

def bestseller_scrapper(url):
    """Scrapes an bestseller page and returns list of products"""
    print(f"Scrapping URL: {url}")

    # step-1 fetch HTML content
    response = requests.get(url, headers=HEADERS)

    if response.status_code != 200:
        print(f"Error: Failed to fetch page. Status code: {response.status_code}")
        return []

    # step-2 parse HTML with BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')

    # step-3 find product containers
    products = []
    product_containers = soup.find_all('div', id='gridItemRoot')

    print(f"Found {len(product_containers)} products")

    for container in product_containers:

        # step-4 extract data
        product_link = container.find('a', class_='a-link-normal')
        title = container.find('div', class_='_cDEzb_p13n-sc-css-line-clamp-1_1Fn1y').get_text(strip=True)
        href = product_link['href'] if product_link else ''
        asin = href.split('/dp/')[1].split("/")[0] if '/dp/' in href else 'N/A'

        image_tag = container.find('img')
        image_url = image_tag['src'] if image_tag else 'N/A'

        rating_span = container.find('span', class_='a-icon-alt')
        rating = rating_span.get_text(strip=True) if rating_span else '0 out of 5 starts'


        products.append({
            'asin' : asin,
            'title' : title,
            'image_url' : image_url,
            'rating' : rating
        })

    return products


if __name__ == "__main__":
    result = bestseller_scrapper(URL)

    if result:
        print("\n Scrapping success")
        print(json.dumps(result, indent=2))
        print(f"\n Total products scrapper: {len(result)}")