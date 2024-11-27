# Skroutz Web Crawler

  

This Python project is a web scraper for **Skroutz.gr**, designed to extract product and store information from specific product categories. It helps users scrape data about products, their availability, prices, and store details, and saves the data into a CSV file.

  

---

  

## Features

  

-  **Product scraping**: Extracts product names and links from a category page.

-  **Store scraping**: Fetches store availability, price, and links for a selected product.

-  **Data storage**: Saves the extracted data into a `CSV` file for further analysis or reference.

-  **Configurable target URL**: The user can change the URL being scraped to fetch data for different categories.

  

---

## Installation

  

### Prerequisites

  

1.  **Python**: Ensure Python 3.8 or higher is installed on your system.

- [Download Python](https://www.python.org/downloads/)

2.  **Pip**: Python package manager (comes pre-installed with Python 3.4+).

  
  

### Steps

1. Clone this repository:

	```bash

	git clone https://github.com/spy-jim/web-scraper-skroutz.git
	```

2. Navigate to the project directory:

	```bash

	cd web-scraper-skroutz
	```

3. Install the required dependencies:

	```bash

	pip install -r requirements.txt
	```
  
---


## Usage

### Running the Script
1.  Execute the script:
	```bash
	python headless_crawler.py
	```
2. The script will display a list of products available on the page. Example:
	```markdown
	Available Products:
	3. Gaggia Classic Pro - Model A
	4. Gaggia Classic Pro - Model B 
	5. Gaggia Classic Pro - Model C
	```
3. Enter the number corresponding to the product you'd like to scrape:
	```mathematica
	Enter the number of the product you want: 1 
	```
4. The script will fetch store details for the selected product and save the data in a file named `skroutz_data.csv`

### Changing the Scraped URL
To scrape a different product category or page:

1. Open the script file (`headless_crawler.py`) in any txt editor.
2. Locate this line in the `__main__` section:
	```python
		target_url = "https://www.skroutz.gr/c/2413/espresso-coffee-machines/m/181/Gaggia.html?cf=gaggia+classis+pro&keyphrase=classic+pro"
	```
3. Replace the URL with your desired search in Skroutz page URL. For example:
	```python
	target_url = "https://www.skroutz.gr/c/2423/laptops/l/132/MacBook.html"
	```
4. Save the file and rerun the script.

---

## Requirements

- Python 3.8 or higher 
- Required libraries:
	- `requests`
	- `beautifulsoup4`
	- `fake-useragent`
- To install the dependencies, run:
	```bash
	pip install -r requirements.txt
---

## Output

- The script saves store data into a CSV file named `skroutz_data.csv`.
- Each row in the CSV contains: 
	- **Store ID**: The unique identifier for the store.
	- **Availability**: The availability status of the product in the store.
	- **Link**: The direct link to the product in the store. 
	- **Price**: The price of the product in the store. Example output: 
	```csv 
	id,availability,link,price 
	store_1234,In Stock,https://www.skroutz.gr/store1234/product-link,€150 
	store_5678,Out of Stock,https://www.skroutz.gr/store5678/product-link,€140
---
## Notes
1. **Be mindful of website terms of service.** Ensure your scraping activities are compliant with Skroutz.gr policies. Can be found here: `https://www.skroutz.gr/robots.txt`
2. **Add delays between requests.** The script includes `time.sleep(2)` to avoid sending rapid consecutive requests.
---

## License
This project is licensed under the MIT License.
Feel free to fork this repository and adapt the code for your needs.

