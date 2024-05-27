import sys
import os
import logging
import pandas as pd

# Logging configuration
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')


def list_backups(backup_dir):
    """List all backup files in the specified backup directory."""
    try:
        backups = [f for f in os.listdir(backup_dir) if os.path.isfile(os.path.join(backup_dir, f)) and not f.startswith('.')]
        backups.sort()
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

def restore_backup(backup_dir):
    """Restore a backup from the specified directory."""
    backups = list_backups(f"data/backups/{backup_dir}")
    backup_file = choose_backup(backups)
    if backup_file:
        backup_path = os.path.join(f"data/backups/{backup_dir}", backup_file)
        restore_path = os.path.join("data", f"{backup_dir}.csv")
        df = pd.read_csv(backup_path)
        df.to_csv(restore_path, index=False)
        logging.info(f"Restored {backup_dir} data from {backup_path} to {restore_path}")
    else:
        logging.info("No backup file chosen.")

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python restore.py <backup_type>")
        sys.exit(1)

    backup_type = sys.argv[1]
    if backup_type not in ['products', 'categories', 'tags']:
        print("Invalid backup type. Must be one of: products, categories, tags")
        sys.exit(1)

    restore_backup(backup_type)
