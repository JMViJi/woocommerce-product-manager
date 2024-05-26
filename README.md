# WooCommerce Product Manager

This project contains scripts to manage products in a WooCommerce store. It allows you to extract product data, upload it back to the store, and create a backup of the product data.

## Features

- Extract all product data from a WooCommerce store and save it to a CSV file.
- Automatically create a timestamped backup of the CSV file for added security.
- Set backup files to read-only to prevent accidental deletion or modification.
- Upload product data to the WooCommerce store.
- Restore the last backup of the product data.

## Setup

### Prerequisites

- Python 3.x
- Virtual environment (recommended)

### Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/JMViJi/woocommerce-product-manager.git
    cd woocommerce-product-manager
    ```

2. Create and activate a virtual environment:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4. Create a `.env` file with your WooCommerce credentials:
    ```env
    WOO_URL=https://yourstore.com/wp-json/
    CONSUMER_KEY=your_consumer_key
    CONSUMER_SECRET=your_consumer_secret
    ```

### Obtaining WooCommerce API Keys

To obtain the API keys for your WooCommerce store, follow these steps:

1. Log in to your WooCommerce store's WordPress admin dashboard.
2. Go to **WooCommerce > Settings**.
3. Click on the **Advanced** tab, then select **REST API**.
4. Click the **Add Key** button.
5. Fill in the **Description** (e.g., "Product Manager Script").
6. Select the **User** you want to generate the key for in the **User** field.
7. Set **Permissions** to **Read/Write**.
8. Click the **Generate API Key** button.
9. You will be shown a **Consumer Key** and a **Consumer Secret**. Copy these keys and paste them into your `.env` file as `CONSUMER_KEY` and `CONSUMER_SECRET`, respectively.

## Usage

### Extract Products

This script fetches all product data from the WooCommerce store, saves it to a CSV file, and creates a timestamped backup of the CSV file.

```bash
python src/extract.py
```

### Upload Products

This script uploads product data to the WooCommerce store.

```bash
python src/upload.py
```

### Create Backup

Although the `extract.py` script already creates a backup when run, you can use the `backup.py` script independently if needed.

```bash
python src/backup.py
```

## Detailed Script Descriptions

### `extract.py`

- **Fetch Product Data:** The script connects to the WooCommerce API and retrieves all product data.
- **Save to CSV:** The fetched product data is saved to `data/products.csv`.
- **Create Backup:** A timestamped backup of the CSV file is created in the `data/` directory. The backup file is named `products_backup_YYYYMMDD_HHMMSS.csv` and is set to read-only to prevent accidental deletion or modification.

### `upload.py`

- **Upload Products:** This script uploads product data to the WooCommerce store. It reads product data from a file and uses the WooCommerce API to update the store.

### `backup.py`

- **Create Backup:** Independently create a backup of the current product data file. The backup file is stored in the `data/` directory with a timestamp in the filename.

## Project Structure

```
woocommerce-product-manager/
│
├── src/
│   ├── backup.py
│   ├── config.py
│   ├── extract.py
│   ├── upload.py
│   └── utils.py
│
├── data/
│   └── products.csv  # This directory will contain the product CSV and backup files
│
├── .gitignore
├── README.md
├── requirements.txt
└── .env
```