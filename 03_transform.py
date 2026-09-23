from pathlib import Path
import logging

import pandas as pd
import yaml

from transformations.transform_customer import (
    transform_customers,
    deduplicate_customers
)

from transformations.transform_product import (
    transform_products,
    deduplicate_products
)

from transformations.transform_store import (
    transform_stores,
    deduplicate_stores
)

from transformations.transform_order import (
    transform_orders,
    deduplicate_orders
)

from validate_customer import split_customer_data
from validate_product import split_product_data
from validate_store import split_store_data
from validate_order import split_order_data


# ============================================================
# PROJECT PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parents[1]
CONFIG_PATH = BASE_DIR / "config" / "config.yaml"


# ============================================================
# LOAD CONFIGURATION
# ============================================================

with open(CONFIG_PATH, "r", encoding="utf-8") as file:
    config = yaml.safe_load(file)


RAW_DIR = BASE_DIR / config["paths"]["raw"]
PROCESSED_DIR = BASE_DIR / config["paths"]["processed"]
REJECTED_DIR = BASE_DIR / config["paths"]["rejected"]


PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
REJECTED_DIR.mkdir(parents=True, exist_ok=True)


# ============================================================
# LOGGING
# ============================================================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


# ============================================================
# LOAD RAW CSV
# ============================================================

def load_csv(file_name: str) -> pd.DataFrame:

    file_path = RAW_DIR / file_name

    if not file_path.exists():
        raise FileNotFoundError(
            f"Raw file not found: {file_path}"
        )

    logger.info("Loading: %s", file_path)

    df = pd.read_csv(file_path)

    logger.info(
        "Loaded: %s rows x %s columns",
        len(df),
        len(df.columns)
    )

    return df


# ============================================================
# SAVE VALID + REJECTED DATA
# ============================================================

def save_data(
    valid_df: pd.DataFrame,
    rejected_df: pd.DataFrame,
    clean_file_name: str,
    rejected_file_name: str
):

    clean_file = PROCESSED_DIR / clean_file_name
    rejected_file = REJECTED_DIR / rejected_file_name

    valid_df.to_csv(
        clean_file,
        index=False
    )

    rejected_df.to_csv(
        rejected_file,
        index=False
    )

    logger.info(
        "Clean data saved: %s",
        clean_file
    )

    logger.info(
        "Rejected data saved: %s",
        rejected_file
    )


# ============================================================
# CUSTOMER PIPELINE
# ============================================================

def process_customers(
    df: pd.DataFrame
):

    logger.info(
        "========== CUSTOMER PIPELINE STARTED =========="
    )

    logger.info(
        "Starting customer transformation."
    )

    transformed_customers = transform_customers(df)

    logger.info(
        "Customer transformation completed."
    )

    logger.info(
        "Starting customer validation."
    )

    valid_customers, rejected_customers = split_customer_data(
        transformed_customers
    )

    logger.info(
    "Valid customers before deduplication: %s",
    len(valid_customers)
    )

    valid_customers = deduplicate_customers(
        valid_customers
    )
    
    logger.info(
        "Valid customers after deduplication: %s",
        len(valid_customers)
    )

    logger.info(
        "Customer validation completed."
    )

    logger.info(
        "Valid customers: %s",
        len(valid_customers)
    )

    logger.info(
        "Rejected customers: %s",
        len(rejected_customers)
    )

    logger.info(
        "========== CUSTOMER PIPELINE COMPLETED =========="
    )

    return valid_customers, rejected_customers


# ============================================================
# PRODUCT PIPELINE
# ============================================================

def process_products(
    df: pd.DataFrame
):

    logger.info(
        "========== PRODUCT PIPELINE STARTED =========="
    )

    logger.info(
        "Starting product transformation."
    )

    transformed_products = transform_products(df)

    logger.info(
        "Product transformation completed."
    )

    logger.info(
        "Starting product validation."
    )

    valid_products, rejected_products = split_product_data(
        transformed_products
    )

    logger.info(
    "Valid products before deduplication: %s",
    len(valid_products)
    )
    
    valid_products = deduplicate_products(
        valid_products
    )
    
    logger.info(
        "Valid products after deduplication: %s",
        len(valid_products)
    )

    logger.info(
        "Product validation completed."
    )

    logger.info(
        "Valid products: %s",
        len(valid_products)
    )

    logger.info(
        "Rejected products: %s",
        len(rejected_products)
    )

    logger.info(
        "========== PRODUCT PIPELINE COMPLETED =========="
    )

    return valid_products, rejected_products


# ============================================================
# STORE PIPELINE
# ============================================================

def process_stores(
    df: pd.DataFrame
):

    logger.info(
        "========== STORE PIPELINE STARTED =========="
    )

    logger.info(
        "Starting store transformation."
    )

    transformed_stores = transform_stores(df)

    logger.info(
        "Store transformation completed."
    )

    logger.info(
        "Starting store validation."
    )

    valid_stores, rejected_stores = split_store_data(
        transformed_stores
    )

    logger.info(
    "Valid stores before deduplication: %s",
    len(valid_stores)
    )
    
    valid_stores = deduplicate_stores(
        valid_stores
    )
    
    logger.info(
        "Valid stores after deduplication: %s",
        len(valid_stores)
    )

    logger.info(
        "Store validation completed."
    )

    logger.info(
        "Valid stores: %s",
        len(valid_stores)
    )

    logger.info(
        "Rejected stores: %s",
        len(rejected_stores)
    )

    logger.info(
        "========== STORE PIPELINE COMPLETED =========="
    )

    return valid_stores, rejected_stores


# ============================================================
# ORDER PIPELINE
# ============================================================

def process_orders(
    df: pd.DataFrame,
    valid_customer_ids: set,
    valid_product_ids: set,
    valid_store_ids: set
):

    logger.info(
        "========== ORDER PIPELINE STARTED =========="
    )

    logger.info(
        "Starting order transformation."
    )

    transformed_orders = transform_orders(df)

    logger.info(
        "Order transformation completed."
    )

    logger.info(
        "Starting order validation."
    )

    valid_orders, rejected_orders = split_order_data(
        transformed_orders,
        valid_customer_ids,
        valid_product_ids,
        valid_store_ids
    )

    logger.info(
        "Order validation completed."
    )

    # --------------------------------------------------------
    # ORDER DEDUPLICATION
    # --------------------------------------------------------

    logger.info(
        "Valid orders before deduplication: %s",
        len(valid_orders)
    )

    valid_orders, duplicate_rejected_orders = deduplicate_orders(
        valid_orders
    )

    logger.info(
        "Valid orders after deduplication: %s",
        len(valid_orders)
    )

    # Add duplicate orders to rejected orders
    rejected_orders = pd.concat(
        [
            rejected_orders,
            duplicate_rejected_orders
        ],
        ignore_index=True
    )

    logger.info(
        "Total rejected orders after duplicate analysis: %s",
        len(rejected_orders)
    )

    logger.info(
        "Valid orders: %s",
        len(valid_orders)
    )

    logger.info(
        "Rejected orders: %s",
        len(rejected_orders)
    )

    logger.info(
        "========== ORDER PIPELINE COMPLETED =========="
    )

    return valid_orders, rejected_orders


# ============================================================
# MAIN ETL PIPELINE
# ============================================================

def main():

    logger.info(
        "=================================================="
    )

    logger.info(
        "RETAIL ANALYTICS TRANSFORMATION PIPELINE STARTED"
    )

    logger.info(
        "=================================================="
    )

    # --------------------------------------------------------
    # CUSTOMERS
    # --------------------------------------------------------

    raw_customers = load_csv(
        config["files"]["customers"]
    )

    valid_customers, rejected_customers = process_customers(
        raw_customers
    )

    save_data(
        valid_customers,
        rejected_customers,
        config["output"]["customers_clean"],
        "customers_rejected.csv"
    )


    # --------------------------------------------------------
    # PRODUCTS
    # --------------------------------------------------------

    raw_products = load_csv(
        config["files"]["products"]
    )

    valid_products, rejected_products = process_products(
        raw_products
    )

    save_data(
        valid_products,
        rejected_products,
        config["output"]["products_clean"],
        "products_rejected.csv"
    )


    # --------------------------------------------------------
    # STORES
    # --------------------------------------------------------

    raw_stores = load_csv(
        config["files"]["stores"]
    )

    valid_stores, rejected_stores = process_stores(
        raw_stores
    )

    save_data(
        valid_stores,
        rejected_stores,
        config["output"]["stores_clean"],
        "stores_rejected.csv"
    )


    # --------------------------------------------------------
    # VALID REFERENCE IDs
    # --------------------------------------------------------

    valid_customer_ids = set(
        valid_customers["customer_id"]
        .dropna()
    )

    valid_product_ids = set(
        valid_products["product_id"]
        .dropna()
    )

    valid_store_ids = set(
        valid_stores["store_id"]
        .dropna()
    )


    logger.info(
        "Valid customer IDs available: %s",
        len(valid_customer_ids)
    )

    logger.info(
        "Valid product IDs available: %s",
        len(valid_product_ids)
    )

    logger.info(
        "Valid store IDs available: %s",
        len(valid_store_ids)
    )


    # --------------------------------------------------------
    # ORDERS
    # --------------------------------------------------------

    raw_orders = load_csv(
        config["files"]["orders"]
    )

    valid_orders, rejected_orders = process_orders(
        raw_orders,
        valid_customer_ids,
        valid_product_ids,
        valid_store_ids
    )

    save_data(
        valid_orders,
        rejected_orders,
        config["output"]["orders_clean"],
        "orders_rejected.csv"
    )


    # ========================================================
    # FINAL SUMMARY
    # ========================================================

    print("\n")
    print("=" * 65)
    print("RETAIL ANALYTICS TRANSFORMATION SUMMARY")
    print("=" * 65)


    print("\nCustomers")
    print("-" * 65)

    print(
        f"Raw customers       : {len(raw_customers):,}"
    )

    print(
        f"Valid customers     : {len(valid_customers):,}"
    )

    print(
        f"Rejected customers  : {len(rejected_customers):,}"
    )

    print(
        f"Rejection rate      : "
        f"{len(rejected_customers) / len(raw_customers) * 100:.2f}%"
    )


    print("\nProducts")
    print("-" * 65)

    print(
        f"Raw products        : {len(raw_products):,}"
    )

    print(
        f"Valid products      : {len(valid_products):,}"
    )

    print(
        f"Rejected products   : {len(rejected_products):,}"
    )

    print(
        f"Rejection rate      : "
        f"{len(rejected_products) / len(raw_products) * 100:.2f}%"
    )


    print("\nStores")
    print("-" * 65)

    print(
        f"Raw stores          : {len(raw_stores):,}"
    )

    print(
        f"Valid stores        : {len(valid_stores):,}"
    )

    print(
        f"Rejected stores     : {len(rejected_stores):,}"
    )

    print(
        f"Rejection rate      : "
        f"{len(rejected_stores) / len(raw_stores) * 100:.2f}%"
    )


    print("\nOrders")
    print("-" * 65)

    print(
        f"Raw orders          : {len(raw_orders):,}"
    )

    print(
        f"Valid orders        : {len(valid_orders):,}"
    )

    print(
        f"Rejected orders     : {len(rejected_orders):,}"
    )

    print(
        f"Rejection rate      : "
        f"{len(rejected_orders) / len(raw_orders) * 100:.2f}%"
    )


    print("\n" + "=" * 65)


    logger.info(
        "=================================================="
    )

    logger.info(
        "RETAIL ANALYTICS TRANSFORMATION PIPELINE COMPLETED"
    )

    logger.info(
        "==================================================")


# ============================================================
# SCRIPT ENTRY POINT
# ============================================================

if __name__ == "__main__":
    main()