import subprocess
import logging
import sys

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

def upload_products():
    """This function uploads product data to the website."""
    logging.info("Uploading products to the website...")
    try:
        subprocess.run(["python", "src/upload.py"], check=True)
    except subprocess.CalledProcessError as e:
        logging.error(f"Error running upload.py: {e}")
        sys.exit(1)
    except Exception as e:
        logging.error(f"Unexpected error: {e}")

def restore_backup():
    """This function restores the last backup."""
    logging.info("Restoring the last backup...")
    try:
        subprocess.run(["python", "src/backup.py"], check=True)
    except subprocess.CalledProcessError as e:
        logging.error(f"Error running backup.py: {e}")
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
1
def main_menu():
    while True:
        print("\n*** Product Management Menu ***")
        print("1. Fetch product data")
        print("2. Upload products to the website")
        print("3. Restore last backup")
        print("4. Exit the program")
        choice = input("Please choose an option (1, 2, 3, 4): ")
        if choice == '1':
            fetch_products()
        elif choice == '2':
            upload_products()
        elif choice == '3':
            restore_backup()
        elif choice == '4':
            logging.info("Exiting the program...")
            break
        else:
            print("Invalid option, please try again.")

if __name__ == '__main__':
    main_menu()
