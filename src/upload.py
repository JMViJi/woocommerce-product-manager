import logging
import pandas as pd
import csv
from woocommerce import API
from config import WOO_URL, CONSUMER_KEY, CONSUMER_SECRET

# Logging configuration
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def get_wc_api(timeout=50):
    """Create and return a WooCommerce API client instance with a specified timeout."""
    return API(
        url=WOO_URL,
        consumer_key=CONSUMER_KEY,
        consumer_secret=CONSUMER_SECRET,
        version="wc/v3",
        timeout=timeout
    )

def read_data_from_csv(filename):
    """Read data from a CSV file."""
    data = []
    try:
        with open(filename, mode='r', encoding='utf-8') as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                data.append(row)
        logging.info(f"Successfully read {len(data)} records from {filename}")
    except Exception as e:
        logging.error(f"Error reading data from CSV: {e}")
    return data

def format_product_data(product):
    """Format product data to match WooCommerce API requirements."""
    formatted_data = {}
    columns_to_include = [
        'name', 'type', 'status', 'sku', 'price', 'regular_price', 
        'sale_price', 'description', 'short_description', 'categories', 'tags'
    ]
    
    for key, value in product.items():
        if key in columns_to_include:
            if pd.isna(value):
                formatted_data[key] = None
            elif key in ['categories', 'tags']:
                formatted_data[key] = [{'name': name.strip()} for name in value.strip('[]').split(',')] if value else []
            else:
                formatted_data[key] = value

    return formatted_data


def format_category_data(category):
    """Format category data to match WooCommerce API requirements."""
    formatted_data = {
        'name': category['name'],
        'slug': category['slug'] if category.get('slug') else category['name'].lower().replace(' ', '-'),
        'description': category.get('description', '')
    }
    return formatted_data

def format_tag_data(tag):
    """Format tag data to match WooCommerce API requirements."""
    formatted_data = {
        'name': tag['name'],
        'slug': tag['slug'] if tag.get('slug') else tag['name'].lower().replace(' ', '-'),
        'description': tag.get('description', '')
    }
    return formatted_data

def get_existing_tags(api):
    """Retrieve existing tags from WooCommerce."""
    existing_tags = {}
    try:
        response = api.get("products/tags", params={"per_page": 100})
        response.raise_for_status()
        tags = response.json()
        for tag in tags:
            existing_tags[tag['slug']] = tag['id']
        logging.info(f"Retrieved {len(existing_tags)} existing tags from WooCommerce")
    except Exception as e:
        logging.error(f"Failed to retrieve existing tags: {e}")
    return existing_tags

def get_existing_items(api, endpoint):
    """Retrieve existing tags or categories from WooCommerce."""
    existing_items = {}
    try:
        response = api.get(endpoint, params={"per_page": 100})
        response.raise_for_status()
        items = response.json()
        for item in items:
            existing_items[item['slug']] = item['id']
        logging.info(f"Retrieved {len(existing_items)} existing items from {endpoint}")
    except Exception as e:
        logging.error(f"Failed to retrieve existing items from {endpoint}: {e}")
    return existing_items


def update_data_in_woocommerce(api, data, endpoint, format_func):
    """Update data in WooCommerce."""
    for item in data:
        formatted_data = format_func(item)
        try:
            logging.debug(f"Uploading data: {formatted_data}")
            response = api.post(endpoint, data=formatted_data)
            response.raise_for_status()
            logging.info(f"Data uploaded successfully to {endpoint}: {formatted_data}")
        except Exception as e:
            logging.error(f"Failed to upload data to {endpoint}: {e}")
            logging.debug(f"Request data: {formatted_data}")
            if hasattr(e, 'response') and e.response is not None:
                logging.debug(f"Response content: {e.response.content}")

def update_data_tag_in_woocommerce(api, data, endpoint, format_func, existing_items):
    """Update data in WooCommerce."""
    for item in data:
        formatted_data = format_func(item)
        slug = formatted_data.get('slug')
        if slug in existing_items:
            tag_id = existing_items[slug]
            try:
                logging.debug(f"Updating tag with ID {tag_id}")
                response = api.put(f"{endpoint}/{tag_id}", data=formatted_data)
                response.raise_for_status()
                logging.info(f"Tag updated successfully.")
            except Exception as e:
                logging.error(f"Failed to update tag with ID {tag_id}: {e}")
                if hasattr(e, 'response') and e.response is not None:
                    logging.debug(f"Response content: {e.response.content}")
        else:
            try:
                logging.debug(f"Creating new tag: {formatted_data}")
                response = api.post(endpoint, data=formatted_data)
                response.raise_for_status()
                logging.info(f"Tag created successfully.")
            except Exception as e:
                logging.error(f"Failed to create new tag: {e}")
                if hasattr(e, 'response') and e.response is not None:
                    logging.debug(f"Response content: {e.response.content}")

def update_data_categories_in_woocommerce(api, data, endpoint, format_func, existing_items):
    """Update data in WooCommerce."""
    for item in data:
        formatted_data = format_func(item)
        slug = formatted_data.get('slug')
        if slug in existing_items:
            item_id = existing_items[slug]
            try:
                logging.debug(f"Updating item with ID {item_id}.")
                response = api.put(f"{endpoint}/{item_id}", data=formatted_data)
                response.raise_for_status()
                logging.info(f"Item updated successfully.")
            except Exception as e:
                logging.error(f"Failed to update item with ID {item_id}: {e}")
                logging.debug(f"Request data: {formatted_data}")
                if hasattr(e, 'response') and e.response is not None:
                    logging.debug(f"Response content: {e.response.content}")
        else:
            try:
                logging.debug(f"Creating new item: {formatted_data}")
                response = api.post(endpoint, data=formatted_data)
                response.raise_for_status()
                logging.info(f"Item created successfully: {formatted_data}")
            except Exception as e:
                logging.error(f"Failed to create new item: {e}")
                logging.debug(f"Request data: {formatted_data}")
                if hasattr(e, 'response') and e.response is not None:
                    logging.debug(f"Response content: {e.response.content}")

def upload_products():
    """Upload products to WooCommerce."""
    products = read_data_from_csv('data/products.csv')
    if products:
        wc_api = get_wc_api()
        update_data_in_woocommerce(wc_api, products, 'products', format_product_data)

def upload_categories():
    """Upload categories to WooCommerce."""
    categories = read_data_from_csv('data/categories.csv')
    if categories:
        wc_api = get_wc_api()
        existing_categories = get_existing_items(wc_api, 'products/categories')
        update_data_categories_in_woocommerce(wc_api, categories, 'products/categories', format_category_data, existing_categories)


def upload_tags():
    """Upload tags to WooCommerce."""
    tags = read_data_from_csv('data/tags.csv')
    if tags:
        wc_api = get_wc_api()
        existing_tags = get_existing_tags(wc_api)
        update_data_tag_in_woocommerce(wc_api, tags, 'products/tags', format_tag_data, existing_tags)

if __name__ == '__main__':
    import sys
    if len(sys.argv) != 2:
        print("Usage: python upload.py [products|categories|tags]")
        sys.exit(1)

    option = sys.argv[1]
    if option == 'products':
        upload_products()
    elif option == 'categories':
        upload_categories()
    elif option == 'tags':
        upload_tags()
    else:
        print("Invalid option. Use 'products', 'categories', or 'tags'.")
        sys.exit(1)
