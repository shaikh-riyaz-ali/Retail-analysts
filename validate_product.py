import pandas as pd


# ============================================================
# 1. Validate Product Unit Price
# ============================================================

def validate_product_unit_price(
    df: pd.DataFrame,
    min_price: float
) -> pd.Series:

    return (
        df["unit_price"].notna()
        & (df["unit_price"] >= min_price)
    )


# ============================================================
# 2. Validate Product Category
# ============================================================

def validate_product_category(
    df: pd.DataFrame,
    allowed_values: list[str]
) -> pd.Series:

    return df["category"].isin(allowed_values)


# ============================================================
# 3. Overall Product Validation
# ============================================================

def validate_products(
    df: pd.DataFrame
) -> pd.Series:

    valid_unit_price = validate_product_unit_price(
        df,
        min_price=0
    )

    valid_category = validate_product_category(
        df,
        allowed_values=[
            "Electronics",
            "Home",
            "Fashion",
            "Beauty",
            "Sports"
        ]
    )

    valid_product = (
        valid_unit_price
        & valid_category
    )

    return valid_product


# ============================================================
# 4. Generate Product Rejection Reasons
# ============================================================

def get_product_rejection_reasons(
    df: pd.DataFrame
) -> pd.Series:

    valid_unit_price = validate_product_unit_price(
        df,
        min_price=0
    )

    valid_category = validate_product_category(
        df,
        allowed_values=[
            "Electronics",
            "Home",
            "Fashion",
            "Beauty",
            "Sports"
        ]
    )

    reasons = pd.Series(
        "",
        index=df.index,
        dtype="string"
    )

    reasons = reasons.mask(
        ~valid_unit_price,
        reasons + "Invalid unit price; "
    )

    reasons = reasons.mask(
        ~valid_category,
        reasons + "Invalid category; "
    )

    return reasons.str.rstrip("; ")


# ============================================================
# 5. Split Valid and Rejected Products
# ============================================================

def split_product_data(
    df: pd.DataFrame
) -> tuple[pd.DataFrame, pd.DataFrame]:

    valid_mask = validate_products(df)

    rejection_reasons = get_product_rejection_reasons(df)

    valid_products = df[valid_mask].copy()

    rejected_products = df[~valid_mask].copy()

    rejected_products["rejection_reason"] = (
        rejection_reasons[~valid_mask]
    )

    return valid_products, rejected_products


# ============================================================
# 6. Test Script
# ============================================================

if __name__ == "__main__":

    df = pd.DataFrame({
        "product_id": [
            "P001",
            "P002",
            "P003",
            "P004"
        ],

        "product_name": [
            "Laptop",
            "Mobile Phone",
            "Headphones",
            "Running Shoes"
        ],

        "category": [
            "Electronics",
            "Electronics",
            "Invalid Category",
            "Fashion"
        ],

        "brand": [
            "Samsung",
            "Apple",
            "Sony",
            "Nike"
        ],

        "unit_price": [
            55000,
            -100,
            2499.50,
            None
        ]
    })

    # --------------------------------------------------------
    # Overall validation
    # --------------------------------------------------------

    valid_products_mask = validate_products(df)

    print("\nOverall Product Validation")
    print("-" * 40)
    print(valid_products_mask)

    # --------------------------------------------------------
    # Rejection reasons
    # --------------------------------------------------------

    rejection_reasons = get_product_rejection_reasons(df)

    print("\nRejection Reasons")
    print("-" * 40)
    print(rejection_reasons)

    # --------------------------------------------------------
    # Split valid and rejected
    # --------------------------------------------------------

    valid_products, rejected_products = (
        split_product_data(df)
    )

    print("\nValid Products")
    print("-" * 40)
    print(valid_products)

    print("\nRejected Products")
    print("-" * 40)
    print(rejected_products)

    # --------------------------------------------------------
    # Summary
    # --------------------------------------------------------

    print("\nValidation Summary")
    print("-" * 40)

    print(f"Total products    : {len(df)}")
    print(f"Valid products    : {len(valid_products)}")
    print(f"Rejected products : {len(rejected_products)}")