import pandas as pd


# ============================================================
# 1. Validate Store Type
# ============================================================

def validate_store_type(
    df: pd.DataFrame,
    allowed_values: list[str]
) -> pd.Series:

    return df["store_type"].isin(allowed_values)


# ============================================================
# 2. Overall Store Validation
# ============================================================

def validate_stores(
    df: pd.DataFrame
) -> pd.Series:

    valid_store_type = validate_store_type(
        df,
        allowed_values=[
            "Flagship",
            "Standard",
            "Express",
            "Outlet"
        ]
    )

    valid_store = valid_store_type

    return valid_store


# ============================================================
# 3. Generate Store Rejection Reasons
# ============================================================

def get_store_rejection_reasons(
    df: pd.DataFrame
) -> pd.Series:

    valid_store_type = validate_store_type(
        df,
        allowed_values=[
            "Flagship",
            "Standard",
            "Express",
            "Outlet"
        ]
    )

    reasons = pd.Series(
        "",
        index=df.index,
        dtype="string"
    )

    reasons = reasons.mask(
        ~valid_store_type,
        reasons + "Invalid store type; "
    )

    return reasons.str.rstrip("; ")


# ============================================================
# 4. Split Valid and Rejected Stores
# ============================================================

def split_store_data(
    df: pd.DataFrame
) -> tuple[pd.DataFrame, pd.DataFrame]:

    valid_mask = validate_stores(df)

    rejection_reasons = get_store_rejection_reasons(df)

    valid_stores = df[valid_mask].copy()

    rejected_stores = df[~valid_mask].copy()

    rejected_stores["rejection_reason"] = (
        rejection_reasons[~valid_mask]
    )

    return valid_stores, rejected_stores


# ============================================================
# 5. Test Script
# ============================================================

if __name__ == "__main__":

    df = pd.DataFrame({
        "store_id": [
            "S001",
            "S002",
            "S003",
            "S004"
        ],

        "store_name": [
            "Bangalore Main",
            "Mumbai Store",
            "Delhi Outlet",
            "Chennai Store"
        ],

        "store_type": [
            "Flagship",
            "Standard",
            "Invalid Type",
            None
        ],

        "city": [
            "Bangalore",
            "Mumbai",
            "Delhi",
            "Chennai"
        ],

        "region": [
            "South",
            "West",
            "North",
            "South"
        ]
    })

    # --------------------------------------------------------
    # Overall validation
    # --------------------------------------------------------

    valid_stores_mask = validate_stores(df)

    print("\nOverall Store Validation")
    print("-" * 40)
    print(valid_stores_mask)

    # --------------------------------------------------------
    # Rejection reasons
    # --------------------------------------------------------

    rejection_reasons = get_store_rejection_reasons(df)

    print("\nRejection Reasons")
    print("-" * 40)
    print(rejection_reasons)

    # --------------------------------------------------------
    # Split valid and rejected
    # --------------------------------------------------------

    valid_stores, rejected_stores = (
        split_store_data(df)
    )

    print("\nValid Stores")
    print("-" * 40)
    print(valid_stores)

    print("\nRejected Stores")
    print("-" * 40)
    print(rejected_stores)

    # --------------------------------------------------------
    # Summary
    # --------------------------------------------------------

    print("\nValidation Summary")
    print("-" * 40)

    print(f"Total stores    : {len(df)}")
    print(f"Valid stores    : {len(valid_stores)}")
    print(f"Rejected stores : {len(rejected_stores)}")