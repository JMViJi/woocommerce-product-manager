import os
import logging
import sys
from upload import read_products_from_csv, update_products_in_woocommerce
from config import WOO_URL, CONSUMER_KEY, CONSUMER_SECRET

# Configuración del logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def list_backups(backup_dir="data/backups"):
    """List all backup files in the backup directory, excluding .gitkeep."""
    try:
        backups = [f for f in os.listdir(backup_dir) if os.path.isfile(os.path.join(backup_dir, f)) and f != '.gitkeep']
        backups = [f for f in backups if not f.startswith('.')]  # Exclude hidden files and .gitkeep
        backups.sort()  # Sort backups by name (which includes timestamp)
        return backups
    except Exception as e:
        logging.error(f"Error listing backup files: {e}")
        return []

def choose_backup(backups):
    """Prompt the user to choose a backup file from the list."""
    if not backups:
        print("No backup files found.")
        return None

    print("Available backup files:")
    for i, backup in enumerate(backups, 1):
        print(f"{i}. {backup}")

    try:
        choice = int(input("Enter the number of the backup file to restore: ")) - 1
        if 0 <= choice < len(backups):
            return backups[choice]
        else:
            print("Invalid choice.")
            return None
    except ValueError:
        print("Invalid input.")
        return None

def main():
    backups = list_backups()
    backup_file = choose_backup(backups)
    if backup_file:
        backup_path = os.path.join("data/backups", backup_file)
        products = read_products_from_csv(backup_path)
        if products:
            update_products_in_woocommerce(products)
        else:
            logging.info("No products found in the backup file.")
    else:
        logging.info("No backup file chosen.")

if __name__ == "__main__":
    main()
