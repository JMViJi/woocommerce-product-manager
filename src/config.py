from dotenv import load_dotenv
import os

# Load environment variables from the .env file
load_dotenv()

# WooCommerce API credentials
WOO_URL = os.getenv('WOO_URL')
CONSUMER_KEY = os.getenv('CONSUMER_KEY')
CONSUMER_SECRET = os.getenv('CONSUMER_SECRET')

# WordPress credentials
WORDPRESS_URL = os.getenv('WORDPRESS_URL')
WORDPRESS_USER = os.getenv('WORDPRESS_USER')
WORDPRESS_PASSWORD = os.getenv('WORDPRESS_PASSWORD')

# WooCommerce API version
VERSION = "wc/v3"
