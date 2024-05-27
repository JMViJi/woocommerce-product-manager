import subprocess
import logging
import sys
from src.utils import fetch_categories, fetch_tags

# Logging configuration
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def fetch_products():
    """This function fetches product data."""
    logging.info("Fetching product data...")
    try:
        subprocess.run(["python", "src/extract.py"], check=True)
    except subprocess.CalledProcessError as e:
        logging.error(f"Error running extract.py: {e}")
    except Exception as e:
        logging.error(f"Unexpected error: {e}")

def upload_data(option):
    """This function uploads data to the website."""
    logging.info(f"Uploading {option} to the website...")
    try:
        subprocess.run(["python", f"src/upload.py", option], check=True)
    except subprocess.CalledProcessError as e:
        logging.error(f"Error running upload.py 3 with option {option}: {e}")
        sys.exit(1)
    except Exception as e:
        logging.error(f"Unexpected error: {e}")

def restore_backup():
    """This function restores a backup."""
    logging.info("Restoring a backup...")
    backup_type = input("Which backup do you want to restore? (1: Products, 2: Categories, 3: Tags, 4: Return to Product Management Menu): ")
    
    if backup_type == '1':
        backup_dir = "products"
    elif backup_type == '2':
        backup_dir = "categories"
    elif backup_type == '3':
        backup_dir = "tags"
    elif backup_type == '4':
        logging.info("Returning to main menu...")
        return
    else:
        print("Invalid option.")

    subprocess.run(["python", "src/restore.py", backup_dir], check=True)

def main_menu():

    while True:
        print("\n*** Product Management Menu ***")
        print("1. Fetch product data")
        print("2. Fetch product categories")
        print("3. Fetch product tags")
        print("4. Upload to the website")
        print("5. Restore backup")
        print("6. Exit the program")
        choice = input("Please choose an option (1, 2, 3, 4, 5, 6): ")
        if choice == '1':
            fetch_products()
        elif choice == '2':
            fetch_categories()
        elif choice == '3':
            fetch_tags()
        elif choice == '4':
            while True:
                print("\n*** Upload Menu ***")
                print("1. Upload products")
                print("2. Upload categories")
                print("3. Upload tags")
                print("4. Back to main menu")
                upload_choice = input("Please choose an option (1, 2, 3, 4): ")
                if upload_choice == '1':
                    upload_data('products')
                elif upload_choice == '2':
                    upload_data('categories')
                elif upload_choice == '3':
                    upload_data('tags')
                elif upload_choice == '4':
                    break
                else:
                    print("Invalid option, please try again.")
        elif choice == '5':
            restore_backup()
        elif choice == '6':
            logging.info("Exiting the program...")
            break
        else:
            print("Invalid option, please try again.")

if __name__ == '__main__':
    main_menu()
