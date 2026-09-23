from pathlib import Path
import logging

import pandas as pd
import yaml


# ============================================================
# PATHS & CONFIGURATION
# ============================================================

BASE_DIR = Path(__file__).resolve().parents[1]

CONFIG_PATH = BASE_DIR / "config" / "config.yaml"
RULES_PATH = BASE_DIR / "config" / "business_rules.yaml"

with open(CONFIG_PATH, "r", encoding="utf-8") as file:
    config = yaml.safe_load(file)

with open(RULES_PATH, "r", encoding="utf-8") as file:
    rules = yaml.safe_load(file)

PROCESSED_DIR = BASE_DIR / config["paths"]["processed"]


# ============================================================
# LOGGING
# ============================================================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


# ============================================================
# LOAD PROCESSED DATA
# ============================================================

def load_processed_data() -> dict[str, pd.DataFrame]:
    """
    Load all cleaned datasets from the processed directory.
    """

    files = {
        "customers": config["output"]["customers_clean"],
        "products": config["output"]["products_clean"],
        "stores": config["output"]["stores_clean"],
        "orders": config["output"]["orders_clean"]
    }

    dataframes = {}

    for entity_name, file_name in files.items():

        file_path = PROCESSED_DIR / file_name

        if not file_path.exists():
            raise FileNotFoundError(
                f"Processed file not found: {file_path}"
            )

        logger.info("Loading: %s", file_path)

        dataframes[entity_name] = pd.read_csv(
            file_path
        )

    return dataframes


# ============================================================
# REQUIRED COLUMN VALIDATION
# ============================================================

def validate_required_columns(
    df: pd.DataFrame,
    required_columns: list[str],
    entity_name: str
) -> bool:

    missing_columns = [
        column
        for column in required_columns
        if column not in df.columns
    ]

    if missing_columns:

        logger.error(
            "%s missing columns: %s",
            entity_name,
            missing_columns
        )

        return False

    return True


# ============================================================
# PRIMARY / BUSINESS KEY VALIDATION
# ============================================================

def validate_unique_key(
    df: pd.DataFrame,
    key_column: str,
    entity_name: str
) -> bool:

    missing_keys = df[key_column].isna().sum()

    duplicate_keys = df[key_column].duplicated().sum()

    logger.info(
        "%s - Missing %s: %s",
        entity_name,
        key_column,
        missing_keys
    )

    logger.info(
        "%s - Duplicate %s: %s",
        entity_name,
        key_column,
        duplicate_keys
    )

    return (
        missing_keys == 0
        and duplicate_keys == 0
    )


# ============================================================
# FOREIGN KEY VALIDATION
# ============================================================

def validate_foreign_key(
    orders: pd.DataFrame,
    reference_df: pd.DataFrame,
    foreign_key: str,
    reference_key: str,
    relationship_name: str
) -> bool:

    valid_ids = set(
        reference_df[reference_key].dropna()
    )

    invalid_count = (
        ~orders[foreign_key].isin(valid_ids)
    ).sum()

    logger.info(
        "%s - Invalid references: %s",
        relationship_name,
        invalid_count
    )

    return invalid_count == 0


# ============================================================
# CUSTOMER VALIDATION
# ============================================================

def validate_customers(
    df: pd.DataFrame
) -> bool:

    logger.info("Validating customers...")

    required_columns = [
        "customer_id",
        "customer_name",
        "gender",
        "age",
        "email",
        "phone",
        "city",
        "signup_date"
    ]

    result = validate_required_columns(
        df,
        required_columns,
        "Customers"
    )

    if not result:
        return False

    return validate_unique_key(
        df,
        "customer_id",
        "Customers"
    )


# ============================================================
# PRODUCT VALIDATION
# ============================================================

def validate_products(
    df: pd.DataFrame
) -> bool:

    logger.info("Validating products...")

    required_columns = [
        "product_id",
        "product_name",
        "category",
        "brand",
        "unit_price"
    ]

    result = validate_required_columns(
        df,
        required_columns,
        "Products"
    )

    if not result:
        return False

    key_valid = validate_unique_key(
        df,
        "product_id",
        "Products"
    )

    price_valid = (
        df["unit_price"].notna()
        & (df["unit_price"] >= 0)
    ).all()

    logger.info(
        "Products - Unit price valid: %s",
        price_valid
    )

    return key_valid and price_valid


# ============================================================
# STORE VALIDATION
# ============================================================

def validate_stores(
    df: pd.DataFrame
) -> bool:

    logger.info("Validating stores...")

    required_columns = [
        "store_id",
        "store_name",
        "store_city",
        "store_region",
        "store_type"
    ]

    result = validate_required_columns(
        df,
        required_columns,
        "Stores"
    )

    if not result:
        return False

    return validate_unique_key(
        df,
        "store_id",
        "Stores"
    )


# ============================================================
# ORDER VALIDATION
# ============================================================

def validate_orders(
    orders: pd.DataFrame,
    customers: pd.DataFrame,
    products: pd.DataFrame,
    stores: pd.DataFrame
) -> bool:

    logger.info("Validating orders...")

    required_columns = [
        "order_id",
        "order_date",
        "customer_id",
        "product_id",
        "store_id",
        "quantity",
        "unit_price",
        "discount",
        "tax",
        "total_amount",
        "payment_method",
        "payment_status",
        "order_status",
        "sales_channel"
    ]

    result = validate_required_columns(
        orders,
        required_columns,
        "Orders"
    )

    if not result:
        return False

    # --------------------------------------------------------
    # Order ID uniqueness
    # --------------------------------------------------------

    order_id_valid = validate_unique_key(
        orders,
        "order_id",
        "Orders"
    )

    # --------------------------------------------------------
    # Quantity
    # --------------------------------------------------------

    quantity_valid = (
        orders["quantity"].notna()
        & (orders["quantity"] >= 1)
    ).all()

    logger.info(
        "Orders - Quantity valid: %s",
        quantity_valid
    )

    # --------------------------------------------------------
    # Unit Price
    # --------------------------------------------------------

    unit_price_valid = (
        orders["unit_price"].notna()
        & (orders["unit_price"] >= 0)
    ).all()

    logger.info(
        "Orders - Unit price valid: %s",
        unit_price_valid
    )

    # --------------------------------------------------------
    # Discount
    # --------------------------------------------------------

    discount_valid = (
        orders["discount"].notna()
        & orders["discount"].between(0, 1)
    ).all()

    logger.info(
        "Orders - Discount valid: %s",
        discount_valid
    )

    # --------------------------------------------------------
    # Order Date
    # --------------------------------------------------------

    order_dates = pd.to_datetime(
        orders["order_date"],
        errors="coerce"
    )

    today = pd.Timestamp.today().normalize()

    date_valid = (
        order_dates.notna()
        & (order_dates <= today)
    ).all()

    logger.info(
        "Orders - Order date valid: %s",
        date_valid
    )

    # --------------------------------------------------------
    # Foreign Keys
    # --------------------------------------------------------

    customer_fk_valid = validate_foreign_key(
        orders,
        customers,
        "customer_id",
        "customer_id",
        "Orders → Customers"
    )

    product_fk_valid = validate_foreign_key(
        orders,
        products,
        "product_id",
        "product_id",
        "Orders → Products"
    )

    store_fk_valid = validate_foreign_key(
        orders,
        stores,
        "store_id",
        "store_id",
        "Orders → Stores"
    )

    return all([
        order_id_valid,
        quantity_valid,
        unit_price_valid,
        discount_valid,
        date_valid,
        customer_fk_valid,
        product_fk_valid,
        store_fk_valid
    ])


# ============================================================
# MAIN VALIDATION PIPELINE
# ============================================================

def main():

    logger.info("=" * 60)
    logger.info("FINAL DATA VALIDATION STARTED")
    logger.info("=" * 60)

    data = load_processed_data()

    customers = data["customers"]
    products = data["products"]
    stores = data["stores"]
    orders = data["orders"]

    # --------------------------------------------------------
    # Dataset summary
    # --------------------------------------------------------

    print()
    print("=" * 65)
    print("PROCESSED DATA SUMMARY")
    print("=" * 65)

    print(f"Customers : {len(customers):,} rows")
    print(f"Products  : {len(products):,} rows")
    print(f"Stores    : {len(stores):,} rows")
    print(f"Orders    : {len(orders):,} rows")

    print("=" * 65)

    # --------------------------------------------------------
    # Entity validation
    # --------------------------------------------------------

    customer_result = validate_customers(
        customers
    )

    product_result = validate_products(
        products
    )

    store_result = validate_stores(
        stores
    )

    order_result = validate_orders(
        orders,
        customers,
        products,
        stores
    )

    # --------------------------------------------------------
    # Final result
    # --------------------------------------------------------

    all_valid = all([
        customer_result,
        product_result,
        store_result,
        order_result
    ])

    print()
    print("=" * 65)
    print("FINAL VALIDATION RESULT")
    print("=" * 65)

    print(
        f"Customers : {'PASS' if customer_result else 'FAIL'}"
    )

    print(
        f"Products  : {'PASS' if product_result else 'FAIL'}"
    )

    print(
        f"Stores    : {'PASS' if store_result else 'FAIL'}"
    )

    print(
        f"Orders    : {'PASS' if order_result else 'FAIL'}"
    )

    print("-" * 65)

    if all_valid:
        print("OVERALL RESULT : PASS")
        logger.info("Final validation passed.")
    else:
        print("OVERALL RESULT : FAIL")
        logger.error("Final validation failed.")

    print("=" * 65)

    logger.info("=" * 60)
    logger.info("FINAL DATA VALIDATION COMPLETED")
    logger.info("=" * 60)


if __name__ == "__main__":
    main()