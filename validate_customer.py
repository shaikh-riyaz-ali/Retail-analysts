import pandas as pd


# ============================================================
# 1. Validate Customer Age
# ============================================================

def validate_customer_age(
    df: pd.DataFrame,
    min_age: int,
    max_age: int
) -> pd.Series:

    return (
        df["age"].notna()
        & df["age"].between(min_age, max_age)
    )


# ============================================================
# 2. Validate Customer Phone
# ============================================================

def validate_customer_phone(
    df: pd.DataFrame,
    required_digits: int
) -> pd.Series:

    phone = df["phone"].astype("string")

    return (
        phone.notna()
        & phone.str.fullmatch(
            rf"\d{{{required_digits}}}"
        )
    )


# ============================================================
# 3. Validate Customer Email
# ============================================================

def validate_customer_email(
    df: pd.DataFrame
) -> pd.Series:

    email = df["email"].astype("string")

    email_pattern = (
        r"^[A-Za-z0-9._%+-]+@"
        r"[A-Za-z0-9.-]+\."
        r"[A-Za-z]{2,}$"
    )

    return (
        email.notna()
        & email.str.fullmatch(email_pattern)
    )


# ============================================================
# 4. Validate Customer Gender
# ============================================================

def validate_customer_gender(
    df: pd.DataFrame,
    allowed_values: list[str]
) -> pd.Series:

    return df["gender"].isin(allowed_values)


# ============================================================
# 5. Validate Signup Date
# ============================================================

def validate_signup_date(
    df: pd.DataFrame
) -> pd.Series:

    today = pd.Timestamp.today().normalize()

    signup_date = pd.to_datetime(
        df["signup_date"],
        errors="coerce"
    )

    return (
        signup_date.notna()
        & (signup_date <= today)
    )


# ============================================================
# 6. Overall Customer Validation
# ============================================================

def validate_customers(
    df: pd.DataFrame
) -> pd.Series:

    valid_age = validate_customer_age(
        df,
        min_age=18,
        max_age=100
    )

    valid_phone = validate_customer_phone(
        df,
        required_digits=10
    )

    valid_email = validate_customer_email(df)

    valid_gender = validate_customer_gender(
        df,
        allowed_values=[
            "Male",
            "Female",
            "Unknown"
        ]
    )

    valid_signup_date = validate_signup_date(df)

    valid_customer = (
        valid_age
        & valid_phone
        & valid_email
        & valid_gender
        & valid_signup_date
    )

    return valid_customer


# ============================================================
# 7. Generate Customer Rejection Reasons
# ============================================================

def get_customer_rejection_reasons(
    df: pd.DataFrame
) -> pd.Series:

    valid_age = validate_customer_age(
        df,
        min_age=18,
        max_age=100
    )

    valid_phone = validate_customer_phone(
        df,
        required_digits=10
    )

    valid_email = validate_customer_email(df)

    valid_gender = validate_customer_gender(
        df,
        allowed_values=[
            "Male",
            "Female",
            "Unknown"
        ]
    )

    valid_signup_date = validate_signup_date(df)

    reasons = pd.Series(
        "",
        index=df.index,
        dtype="string"
    )

    reasons = reasons.mask(
        ~valid_age,
        reasons + "Invalid age; "
    )

    reasons = reasons.mask(
        ~valid_phone,
        reasons + "Invalid phone; "
    )

    reasons = reasons.mask(
        ~valid_email,
        reasons + "Invalid email; "
    )

    reasons = reasons.mask(
        ~valid_gender,
        reasons + "Invalid gender; "
    )

    reasons = reasons.mask(
        ~valid_signup_date,
        reasons + "Invalid signup date; "
    )

    return reasons.str.rstrip("; ")


# ============================================================
# 8. Split Valid and Rejected Customers
# ============================================================

def split_customer_data(
    df: pd.DataFrame
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Split customers into valid and rejected records.

    Returns:
        valid_customers
        rejected_customers
    """

    # Overall validation
    valid_mask = validate_customers(df)

    # Generate rejection reasons
    rejection_reasons = get_customer_rejection_reasons(df)

    # Valid records
    valid_customers = df[valid_mask].copy()

    # Rejected records
    rejected_customers = df[~valid_mask].copy()

    # Add rejection reason
    rejected_customers["rejection_reason"] = (
        rejection_reasons[~valid_mask]
    )

    return valid_customers, rejected_customers


# ============================================================
# 9. Test Script
# ============================================================

if __name__ == "__main__":

    # Sample transformed customer data
    df = pd.DataFrame({
        "customer_id": [
            "C001",
            "C002",
            "C003",
            "C004"
        ],

        "age": [
            25,
            -5,
            35,
            45
        ],

        "phone": [
            "9876543210",
            "9123456789",
            "12345",
            "9876543210"
        ],

        "email": [
            "rahul@example.com",
            "priya@gmail.com",
            "invalid-email",
            "amit@example.com"
        ],

        "gender": [
            "Male",
            "Female",
            "Male",
            "Unknown"
        ],

        "signup_date": [
            "2024-01-15",
            "2025-06-20",
            "2024-05-10",
            "2030-01-01"
        ]
    })

    # Convert signup date
    df["signup_date"] = pd.to_datetime(
        df["signup_date"],
        format="mixed",
        errors="coerce"
    )

    # --------------------------------------------------------
    # Overall validation
    # --------------------------------------------------------

    valid_customers_mask = validate_customers(df)

    print("\nOverall Customer Validation")
    print("-" * 40)
    print(valid_customers_mask)

    # --------------------------------------------------------
    # Rejection reasons
    # --------------------------------------------------------

    rejection_reasons = get_customer_rejection_reasons(df)

    print("\nRejection Reasons")
    print("-" * 40)
    print(rejection_reasons)

    # --------------------------------------------------------
    # Split valid and rejected records
    # --------------------------------------------------------

    valid_customers, rejected_customers = split_customer_data(df)

    # --------------------------------------------------------
    # Valid customers
    # --------------------------------------------------------

    print("\nValid Customers")
    print("-" * 40)
    print(valid_customers)

    # --------------------------------------------------------
    # Rejected customers
    # --------------------------------------------------------

    print("\nRejected Customers")
    print("-" * 40)
    print(rejected_customers)

    # --------------------------------------------------------
    # Summary
    # --------------------------------------------------------

    print("\nValidation Summary")
    print("-" * 40)
    print(f"Total customers   : {len(df)}")
    print(f"Valid customers   : {len(valid_customers)}")
    print(f"Rejected customers: {len(rejected_customers)}")