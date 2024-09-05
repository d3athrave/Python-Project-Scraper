import requests
from bs4 import BeautifulSoup
import re

def scrape_product_details(url: str) -> tuple[str | None, list[str], list[str], str | None]:
    """Scrapes product price, available sizes, out-of-stock sizes, and item code from a webpage.

    Args:
        url: The URL of the webpage to scrape.

    Returns:
        A tuple containing the product price, available sizes, out-of-stock sizes, and item code.
    """

    try:
        response = requests.get(url)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')

        # Find price div
        price_div = soup.find('div', class_='product-price--original')
        price = price_div.text.strip() if price_div else None

        # Find size options within select
        select_tag = soup.find('select')
        size_options = select_tag.find_all('option') if select_tag else []

        available_sizes = []
        out_of_stock_sizes = []
        for option in size_options:
            size = option.text.strip()
            if "(Out of stock)" not in size:
                available_sizes.append(size)
            else:
                out_of_stock_sizes.append(size)

        # Find item code in ul within product-page--description div
        description_div = soup.find('div', class_='product-page--description')
        if description_div:
            ul_tag = description_div.find('ul')
            if ul_tag:
                item_code_element = ul_tag.find('li', string=re.compile(r"I0\d{2}_\d{2}_\d{2}"))
                item_code = item_code_element.text.strip() if item_code_element else None
            print(item_code)
        else:
            item_code = None

        return price, available_sizes, out_of_stock_sizes, item_code
    except requests.exceptions.RequestException as e:
        print(f"Error making request: {e}")
        return None, [], [], None

# Example usage:
if __name__ == "__main__":
    # sample for American Rag URL
    url = "https://americanrag.ae/collections/carhartt-wip/products/l-s-master-shirt-for-mens-3?variant=44405048606894"  # Replace with the actual URL
    price, available_sizes, out_of_stock_sizes, item_code = scrape_product_details(url)

    if price and (available_sizes or out_of_stock_sizes):
        print("Product price:", price)
        print("Available sizes:", available_sizes)
        print("Out of stock sizes:", out_of_stock_sizes)
        print("Item code:", item_code)
    else:
        print("Product details not found.")
