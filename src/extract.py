import logging
import os
import pandas as pd
from woocommerce import API
from config import WOO_URL, CONSUMER_KEY, CONSUMER_SECRET
from datetime import datetime


# Logging configuration
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def get_wc_api():
    """Create and return a WooCommerce API client instance."""
    return API(
        url=WOO_URL,
        consumer_key=CONSUMER_KEY,
        consumer_secret=CONSUMER_SECRET,
        version="wc/v3"
    )

def get_variants(wc_api, product_id):
    """Fetch variants for a variable product."""
    try:
        response = wc_api.get(f"products/{product_id}/variations")
        response.raise_for_status()
        return response.json()
    except Exception as e:
        logging.error(f"Error fetching variants for product {product_id}: {e}")
        return []

def get_all_products():
    """Fetch all products from WooCommerce."""
    wc_api = get_wc_api()
    all_products = []
    page = 1
    while True:
        try:
            response = wc_api.get("products", params={"per_page": 100, "page": page})
            response.raise_for_status()
            current_products = response.json()
            if not current_products:
                break  # No more products, end loop
            for product in current_products:
                # If the product is variable, also fetch its variants
                if product['type'] == 'variable':
                    product['variants'] = get_variants(wc_api, product['id'])
                all_products.append(product)
            page += 1  # Increment page for next request
        except Exception as e:
            logging.error(f"Error fetching products on page {page}: {e}")
            break  # Optional: Break on error or decide how to handle errors
    return all_products

def save_products_to_file(products, filename='data/products.csv'):
    """Save product data to a CSV file using pandas."""
    logging.info(f"Saving product data to {filename}...")
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    try:
        # Convert the list of products into a DataFrame
        df = pd.DataFrame(products)
        
        # Save DataFrame to CSV
        df.to_csv(filename, index=False)
        logging.info(f"Product data saved to {filename} successfully.")
        
        # Create a backup of the file
        create_backup(filename)
    except Exception as err:
        logging.error(f"An error occurred while saving product data: {err}")

def create_backup(original_file):
    """Create a backup of the CSV file with a timestamp in the filename."""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_filename = f"data/backups/products_backup_{timestamp}.csv"
    logging.info(f"Creating backup of the file as {backup_filename}...")
    try:
        os.makedirs(os.path.dirname(backup_filename), exist_ok=True)
        with open(original_file, 'rb') as src_file:
            with open(backup_filename, 'wb') as backup_file:
                backup_file.write(src_file.read())
        logging.info(f"Backup created successfully as {backup_filename}.")
        
        # Make the backup file read-only
        os.chmod(backup_filename, 0o444)  # Unix-based systems: read-only for all users
        logging.info(f"Backup file {backup_filename} set to read-only.")
    except Exception as err:
        logging.error(f"An error occurred while creating the backup: {err}")

if __name__ == '__main__':
    products = get_all_products()
    if products:
        save_products_to_file(products)
