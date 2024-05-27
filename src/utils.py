import logging
from woocommerce import API
import pandas as pd
import os
from datetime import datetime
from src.config import WOO_URL, CONSUMER_KEY, CONSUMER_SECRET

# Logging configuration
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')


def get_wc_api(timeout=15):
    """Create and return a WooCommerce API client instance with a specified timeout."""
    return API(
        url=WOO_URL,
        consumer_key=CONSUMER_KEY,
        consumer_secret=CONSUMER_SECRET,
        version="wc/v3",
        timeout=timeout
    )

def save_backup(df, file_prefix, backup_dir):
    """Save a DataFrame to a CSV file and create a timestamped backup."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"data/{file_prefix}.csv"
    backup_filename = f"data/backups/{backup_dir}/{file_prefix}_backup_{timestamp}.csv"

    # Create directories if they don't exist
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    os.makedirs(os.path.dirname(backup_filename), exist_ok=True)

    # Save the current file
    df.to_csv(filename, index=False)
    
    # Save the backup file
    df.to_csv(backup_filename, index=False)

    # Set the backup file to read-only
    os.chmod(backup_filename, 0o444)
    logging.info(f"{file_prefix.capitalize()} data saved and backup created at {backup_filename}")

def fetch_categories():
    """Fetch product categories from WooCommerce and save to a CSV file."""
    logging.info("Fetching product categories...")
    wc_api = get_wc_api()
    try:
        categories = wc_api.get("products/categories").json()
        df = pd.DataFrame(categories)
        save_backup(df, 'categories', 'categories')
    except Exception as e:
        logging.error(f"Error fetching categories: {e}")

def fetch_tags():
    """Fetch product tags from WooCommerce and save to a CSV file."""
    logging.info("Fetching product tags...")
    wc_api = get_wc_api()
    try:
        tags = wc_api.get("products/tags").json()
        df = pd.DataFrame(tags)
        save_backup(df, 'tags', 'tags')
    except Exception as e:
        logging.error(f"Error fetching tags: {e}")
