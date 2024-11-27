from bs4 import BeautifulSoup
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def get_product_page(url, wait_for_shop_info=False):
    """Fetches the product page HTML content.

    Args:
        url (str): The URL of the product page.
        wait_for_shop_info (bool): Whether to wait for the shop-info-row element.

    Returns:
        str: The HTML content of the product page, or None if there's an error.
    """
    try:
        options = Options()
        options.headless = True
        driver = webdriver.Firefox(options=options)

        driver.get(url)

        # Conditionally wait for the specific element that indicates content is fully loaded
        if wait_for_shop_info:
            WebDriverWait(driver, 60).until(
                EC.presence_of_element_located((By.CLASS_NAME, "shop-info-row"))
            )

        # Additional wait to ensure all JavaScript content is loaded
        time.sleep(5)

        html_content = driver.page_source

        driver.quit()

        return html_content

    except Exception as e:
        print(f"Error fetching product page for {url}: {e}")
        driver.quit()
        return None

def get_store_data(html_content):
    """Extracts store information from the provided HTML content.

    Args:
        html_content (str): The HTML content of the product page.

    Returns:
        list: A list of dictionaries, where each dictionary represents a store's
            information (id, availability, link, price).
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    # Find all store cards
    stores = soup.find_all('li', class_=['card js-product-card'])
    store_data = []
    
    for store in stores:
        # Extract store id
        store_id = store.get('id')

        # Extract store availability
        store_availability_element = store.find('p', class_='availability')
        store_availability = store_availability_element.text.strip() if store_availability_element else None

        # Extract store link
        store_link_element = store.find('a', class_='js-product-link')
        store_link = 'https://www.skroutz.gr' + store_link_element.get('href') if store_link_element else None

        # Get price section
        price_section = store.find('div', class_='price')

        # Extract price
        price = price_section.find('strong').text.strip() if price_section else None

        store_data.append({
            'id': store_id,
            'availability': store_availability,
            'link': store_link,
            'price': price
        })

    return store_data

def get_product_list(html_content):
    """Extracts product information from the provided HTML content of a category page.

    Args:
        html_content (str): The HTML content of the category page.

    Returns:
        list: A list of dictionaries, where each dictionary represents a product's
            information (name, link).
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    # Find all product elements (replace with the appropriate class name for product listings)
    products = soup.find_all('li', class_=['cf card', 'cf card with-skus-slider', 'cf card labeled-item labeled-product'])
    product_data = []

    for product in products:
        # Extract product name
        product_name_element = product.find('a', class_='js-sku-link')  # Modify this selector if needed
        product_name = product_name_element.get('title').strip() if product_name_element else None

        # Extract product link
        product_link = 'https://www.skroutz.gr' + product_name_element.get('href') if product_name_element else None

        product_data.append({
            'name': product_name,
            'link': product_link
        })

    return product_data

def save_data(store_data, filename='skroutz_data.csv'):
    """Saves product and store data to a CSV file.

    Args:
        store_data (list): A list of dictionaries, where each dictionary represents a store's
                        information (id, availability, link, price).
        filename (str, optional): The filename for the CSV file. Defaults to 'skroutz_data.csv'.
    """
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)

        # Write header row for store data
        if store_data:
            store_headers = store_data[0].keys()  # Extract headers from first store dictionary
            writer.writerow(store_headers)

        # Write each store's data as a row
        for store in store_data:
            writer.writerow(list(store.values()))

if __name__ == '__main__':
    target_url = "https://www.skroutz.gr/c/2413/espresso-coffee-machines/m/181/Gaggia.html?cf=gaggia+classis+pro&keyphrase=classic+pro"

    # Fetch HTML content of the search page without waiting for shop-info-row
    html_content = get_product_page(target_url, wait_for_shop_info=False)

    if html_content:
        # Debugging output to check if JavaScript content is loaded
        print(html_content[:1000])  # Print the first 1000 characters of the HTML content

        # Get Product list
        product_list = get_product_list(html_content)

        # Display available products
        print("Available Products:")
        for index, product in enumerate(product_list, start=1):
            print(f"{index}. {product['name']}")

        choice = int(input("Enter the number of the product you want: "))
        chosen_product = product_list[choice - 1]

        # Fetch HTML content of the chosen product page with waiting for shop-info-row
        product_html_content = get_product_page(chosen_product['link'], wait_for_shop_info=True)

        if product_html_content:
            # Extract store information
            store_data = get_store_data(product_html_content)
            time.sleep(2)  # Adding delay between requests

            # Save store data to CSV
            save_data(store_data=store_data)  # Pass store_data as keyword argument
        else:
            print("Error fetching product page content.")
    else:
        print("Error fetching search page content.")
