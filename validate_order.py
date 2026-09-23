import pandas as pd


# ============================================================
# BASIC BUSINESS RULE VALIDATIONS
# ============================================================

def validate_order_quantity(
    df: pd.DataFrame,
    min_quantity: int
) -> pd.Series:
    return (
        df["quantity"].notna()
        & (df["quantity"] >= min_quantity)
    )


def validate_order_unit_price(
    df: pd.DataFrame,
    min_price: float
) -> pd.Series:
    return (
        df["unit_price"].notna()
        & (df["unit_price"] >= min_price)
    )


def validate_order_discount(
    df: pd.DataFrame,
    min_discount: float,
    max_discount: float
) -> pd.Series:
    return (
        df["discount"].notna()
        & df["discount"].between(min_discount, max_discount)
    )


def validate_order_date(
    df: pd.DataFrame,
    allow_future_date: bool
) -> pd.Series:

    order_date = pd.to_datetime(
        df["order_date"],
        errors="coerce"
    )

    valid_date = order_date.notna()

    if not allow_future_date:
        today = pd.Timestamp.today().normalize()
        valid_date = valid_date & (order_date <= today)

    return valid_date


# ============================================================
# CATEGORICAL VALIDATIONS
# ============================================================

def validate_payment_method(
    df: pd.DataFrame,
    allowed_values: list[str]
) -> pd.Series:
    return df["payment_method"].isin(allowed_values)


def validate_payment_status(
    df: pd.DataFrame,
    allowed_values: list[str]
) -> pd.Series:
    return df["payment_status"].isin(allowed_values)


def validate_order_status(
    df: pd.DataFrame,
    allowed_values: list[str]
) -> pd.Series:
    return df["order_status"].isin(allowed_values)


def validate_sales_channel(
    df: pd.DataFrame,
    allowed_values: list[str]
) -> pd.Series:
    return df["sales_channel"].isin(allowed_values)


# ============================================================
# FOREIGN KEY VALIDATIONS
# ============================================================

def validate_customer_reference(
    df: pd.DataFrame,
    valid_customer_ids: set
) -> pd.Series:
    return (
        df["customer_id"].notna()
        & df["customer_id"].isin(valid_customer_ids)
    )


def validate_product_reference(
    df: pd.DataFrame,
    valid_product_ids: set
) -> pd.Series:
    return (
        df["product_id"].notna()
        & df["product_id"].isin(valid_product_ids)
    )


def validate_store_reference(
    df: pd.DataFrame,
    valid_store_ids: set
) -> pd.Series:
    return (
        df["store_id"].notna()
        & df["store_id"].isin(valid_store_ids)
    )


# ============================================================
# COMPLETE ORDER VALIDATION
# ============================================================

def validate_orders(
    df: pd.DataFrame,
    valid_customer_ids: set,
    valid_product_ids: set,
    valid_store_ids: set
) -> pd.Series:

    valid_quantity = validate_order_quantity(
        df,
        min_quantity=1
    )

    valid_unit_price = validate_order_unit_price(
        df,
        min_price=0
    )

    valid_discount = validate_order_discount(
        df,
        min_discount=0,
        max_discount=1
    )

    valid_order_date = validate_order_date(
        df,
        allow_future_date=False
    )

    valid_payment_method = validate_payment_method(
        df,
        [
            "Credit Card",
            "Debit Card",
            "UPI",
            "Net Banking",
            "Cash",
            "Wallet"
        ]
    )

    valid_payment_status = validate_payment_status(
        df,
        [
            "Paid",
            "Pending",
            "Failed",
            "Refunded"
        ]
    )

    valid_order_status = validate_order_status(
        df,
        [
            "Completed",
            "Pending",
            "Cancelled",
            "Returned"
        ]
    )

    valid_sales_channel = validate_sales_channel(
        df,
        [
            "Website",
            "Mobile App",
            "Marketplace",
            "Physical Store"
        ]
    )

    valid_customer = validate_customer_reference(
        df,
        valid_customer_ids
    )

    valid_product = validate_product_reference(
        df,
        valid_product_ids
    )

    valid_store = validate_store_reference(
        df,
        valid_store_ids
    )

    return (
        valid_quantity
        & valid_unit_price
        & valid_discount
        & valid_order_date
        & valid_payment_method
        & valid_payment_status
        & valid_order_status
        & valid_sales_channel
        & valid_customer
        & valid_product
        & valid_store
    )


# ============================================================
# REJECTION REASONS
# ============================================================

def get_order_rejection_reasons(
    df: pd.DataFrame,
    valid_customer_ids: set,
    valid_product_ids: set,
    valid_store_ids: set
) -> pd.Series:

    valid_quantity = validate_order_quantity(df, 1)

    valid_unit_price = validate_order_unit_price(df, 0)

    valid_discount = validate_order_discount(
        df,
        min_discount=0,
        max_discount=1
    )

    valid_order_date = validate_order_date(
        df,
        allow_future_date=False
    )

    valid_payment_method = validate_payment_method(
        df,
        [
            "Credit Card",
            "Debit Card",
            "UPI",
            "Net Banking",
            "Cash",
            "Wallet"
        ]
    )

    valid_payment_status = validate_payment_status(
        df,
        [
            "Paid",
            "Pending",
            "Failed",
            "Refunded"
        ]
    )

    valid_order_status = validate_order_status(
        df,
        [
            "Completed",
            "Pending",
            "Cancelled",
            "Returned"
        ]
    )

    valid_sales_channel = validate_sales_channel(
        df,
        [
            "Website",
            "Mobile App",
            "Marketplace",
            "Physical Store"
        ]
    )

    valid_customer = validate_customer_reference(
        df,
        valid_customer_ids
    )

    valid_product = validate_product_reference(
        df,
        valid_product_ids
    )

    valid_store = validate_store_reference(
        df,
        valid_store_ids
    )

    reasons = pd.Series(
        "",
        index=df.index,
        dtype="string"
    )

    reasons = reasons.mask(
        ~valid_quantity,
        reasons + "Invalid quantity; "
    )

    reasons = reasons.mask(
        ~valid_unit_price,
        reasons + "Invalid unit price; "
    )

    reasons = reasons.mask(
        ~valid_discount,
        reasons + "Invalid discount; "
    )

    reasons = reasons.mask(
        ~valid_order_date,
        reasons + "Invalid order date; "
    )

    reasons = reasons.mask(
        ~valid_payment_method,
        reasons + "Invalid payment method; "
    )

    reasons = reasons.mask(
        ~valid_payment_status,
        reasons + "Invalid payment status; "
    )

    reasons = reasons.mask(
        ~valid_order_status,
        reasons + "Invalid order status; "
    )

    reasons = reasons.mask(
        ~valid_sales_channel,
        reasons + "Invalid sales channel; "
    )

    reasons = reasons.mask(
        ~valid_customer,
        reasons + "Invalid customer reference; "
    )

    reasons = reasons.mask(
        ~valid_product,
        reasons + "Invalid product reference; "
    )

    reasons = reasons.mask(
        ~valid_store,
        reasons + "Invalid store reference; "
    )

    return reasons.str.rstrip("; ")


# ============================================================
# SPLIT VALID AND REJECTED ORDERS
# ============================================================

def split_order_data(
    df: pd.DataFrame,
    valid_customer_ids: set,
    valid_product_ids: set,
    valid_store_ids: set
) -> tuple[pd.DataFrame, pd.DataFrame]:

    valid_mask = validate_orders(
        df,
        valid_customer_ids,
        valid_product_ids,
        valid_store_ids
    )

    rejection_reasons = get_order_rejection_reasons(
        df,
        valid_customer_ids,
        valid_product_ids,
        valid_store_ids
    )

    valid_orders = df[valid_mask].copy()

    rejected_orders = df[~valid_mask].copy()

    rejected_orders["rejection_reason"] = (
        rejection_reasons[~valid_mask]
    )

    return valid_orders, rejected_orders


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    test_data = pd.DataFrame({
        "order_id": ["O001", "O002", "O003"],
        "customer_id": ["C001", "C999", "C001"],
        "product_id": ["P001", "P001", "P999"],
        "store_id": ["S001", "S001", "S999"],
        "order_date": [
            "2025-01-10",
            "2025-01-10",
            "2025-01-10"
        ],
        "quantity": [2, 1, -2],
        "unit_price": [500, 100, 200],
        "discount": [0.10, 0.20, 0.10],
        "payment_method": [
            "Credit Card",
            "UPI",
            "Cash"
        ],
        "payment_status": [
            "Paid",
            "Paid",
            "Paid"
        ],
        "order_status": [
            "Completed",
            "Completed",
            "Completed"
        ],
        "sales_channel": [
            "Website",
            "Mobile App",
            "Website"
        ]
    })

    valid_customer_ids = {
        "C001",
        "C002"
    }

    valid_product_ids = {
        "P001",
        "P002"
    }

    valid_store_ids = {
        "S001",
        "S002"
    }

    valid_orders, rejected_orders = split_order_data(
        test_data,
        valid_customer_ids,
        valid_product_ids,
        valid_store_ids
    )

    print("\nValid Orders")
    print("-" * 50)
    print(valid_orders)

    print("\nRejected Orders")
    print("-" * 50)
    print(rejected_orders)