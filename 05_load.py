from pathlib import Path
import logging

import pandas as pd
import pyodbc
import yaml


# ============================================================
# PATHS & CONFIGURATION
# ============================================================

BASE_DIR = Path(__file__).resolve().parents[1]

CONFIG_PATH = BASE_DIR / "config" / "config.yaml"

with open(CONFIG_PATH, "r", encoding="utf-8") as file:
    config = yaml.safe_load(file)

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
# DATABASE CONFIGURATION
# ============================================================

SERVER = r"localhost\SQLEXPRESS"
DATABASE = "RetailAnalytics"
DRIVER = "ODBC Driver 18 for SQL Server"

CONNECTION_STRING = (
    f"DRIVER={{{DRIVER}}};"
    f"SERVER={SERVER};"
    f"DATABASE={DATABASE};"
    "Trusted_Connection=yes;"
    "Encrypt=yes;"
    "TrustServerCertificate=yes;"
)


# ============================================================
# DATABASE CONNECTION
# ============================================================

def get_connection():
    """
    Create and return a SQL Server database connection.
    """

    logger.info(
        "Connecting to SQL Server: %s",
        SERVER
    )

    connection = pyodbc.connect(
        CONNECTION_STRING
    )

    logger.info(
        "Database connection successful."
    )

    return connection


# ============================================================
# LOAD CSV
# ============================================================

def load_csv(file_name: str) -> pd.DataFrame:
    """
    Load a processed CSV file into a pandas DataFrame.
    """

    file_path = PROCESSED_DIR / file_name

    if not file_path.exists():
        raise FileNotFoundError(
            f"Processed file not found: {file_path}"
        )

    logger.info(
        "Loading processed file: %s",
        file_path
    )

    df = pd.read_csv(
        file_path
    )

    logger.info(
        "Loaded %s rows from %s",
        len(df),
        file_name
    )

    return df


# ============================================================
# LOAD DATAFRAME INTO SQL SERVER
# ============================================================

def load_dataframe(
    connection,
    df: pd.DataFrame,
    table_name: str,
    columns: list[str]
) -> None:
    """
    Insert a DataFrame into a SQL Server table.
    """

    logger.info(
        "Loading %s rows into dbo.%s",
        len(df),
        table_name
    )

    column_names = ", ".join(
        f"[{column}]"
        for column in columns
    )

    placeholders = ", ".join(
        "?"
        for _ in columns
    )

    insert_sql = f"""
        INSERT INTO dbo.{table_name}
        ({column_names})
        VALUES ({placeholders})
    """

    cursor = connection.cursor()

    cursor.fast_executemany = True

    rows = [
        tuple(
            None if pd.isna(value) else value
            for value in row
        )
        for row in df[columns].itertuples(
            index=False,
            name=None
        )
    ]

    cursor.executemany(
        insert_sql,
        rows
    )

    connection.commit()

    cursor.close()

    logger.info(
        "Successfully loaded %s rows into dbo.%s",
        len(rows),
        table_name
    )


# ============================================================
# LOAD CUSTOMERS
# ============================================================

def load_customers(connection) -> None:

    df = load_csv(
        config["output"]["customers_clean"]
    )

    columns = [
        "customer_id",
        "customer_name",
        "gender",
        "age",
        "email",
        "phone",
        "city",
        "signup_date"
    ]

    load_dataframe(
        connection,
        df,
        "Customers",
        columns
    )


# ============================================================
# LOAD PRODUCTS
# ============================================================

def load_products(connection) -> None:

    df = load_csv(
        config["output"]["products_clean"]
    )

    columns = [
        "product_id",
        "product_name",
        "category",
        "brand",
        "unit_price"
    ]

    load_dataframe(
        connection,
        df,
        "Products",
        columns
    )


# ============================================================
# LOAD STORES
# ============================================================

def load_stores(connection) -> None:

    df = load_csv(
        config["output"]["stores_clean"]
    )

    columns = [
        "store_id",
        "store_name",
        "store_city",
        "store_region",
        "store_type"
    ]

    load_dataframe(
        connection,
        df,
        "Stores",
        columns
    )


# ============================================================
# LOAD ORDERS
# ============================================================

def load_orders(connection) -> None:

    df = load_csv(
        config["output"]["orders_clean"]
    )

    columns = [
        "order_id",
        "order_date",
        "customer_id",
        "product_id",
        "store_id",
        "quantity",
        "unit_price",
        "discount",
        "tax",
        "shipping_cost",
        "total_amount",
        "payment_method",
        "payment_status",
        "order_status",
        "sales_channel"
    ]

    load_dataframe(
        connection,
        df,
        "Orders",
        columns
    )


# ============================================================
# MAIN ETL LOAD
# ============================================================

def main():

    logger.info("=" * 60)
    logger.info("SQL SERVER LOAD STARTED")
    logger.info("=" * 60)

    connection = None

    try:

        connection = get_connection()

        # Foreign-key dependency order
        load_customers(connection)
        load_products(connection)
        load_stores(connection)
        load_orders(connection)

        logger.info("=" * 60)
        logger.info("SQL SERVER LOAD COMPLETED SUCCESSFULLY")
        logger.info("=" * 60)

    except Exception as error:

        if connection is not None:
            connection.rollback()

        logger.exception(
            "SQL Server load failed: %s",
            error
        )

        raise

    finally:

        if connection is not None:
            connection.close()

            logger.info(
                "Database connection closed."
            )


if __name__ == "__main__":
    main()