from pathlib import Path
import logging

import pandas as pd
import yaml


# ---------------------------------------------------------
# Project paths
# ---------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parents[1]

CONFIG_PATH = BASE_DIR / "config" / "config.yaml"

with open(CONFIG_PATH, "r", encoding="utf-8") as file:
    config = yaml.safe_load(file)


RAW_DIR = BASE_DIR / config["paths"]["raw"]
PROFILE_DIR = BASE_DIR / config["paths"]["profiling"]

PROFILE_DIR.mkdir(parents=True, exist_ok=True)


# ---------------------------------------------------------
# Logging
# ---------------------------------------------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


# ---------------------------------------------------------
# Load raw data
# ---------------------------------------------------------

def load_raw_data(file_name: str) -> pd.DataFrame:
    """Load a raw CSV file into a DataFrame."""

    file_path = RAW_DIR / file_name

    logger.info("Loading file: %s", file_path)

    return pd.read_csv(file_path)


# ---------------------------------------------------------
# Column profile
# ---------------------------------------------------------

def profile_columns(df: pd.DataFrame, entity_name: str) -> pd.DataFrame:
    """Generate basic column-level profiling information."""

    profile = pd.DataFrame({
        "Entity": entity_name,
        "Column": df.columns,
        "Data_Type": df.dtypes.astype(str).values,
        "Row_Count": len(df),
        "Non_Null_Count": df.notna().sum().values,
        "Null_Count": df.isna().sum().values,
        "Null_Percentage": (
            df.isna().mean().values * 100
        ).round(2),
        "Unique_Count": df.nunique(dropna=True).values
    })

    return profile


# ---------------------------------------------------------
# Missing-value profile
# ---------------------------------------------------------

def profile_missing_values(
    df: pd.DataFrame,
    entity_name: str
) -> pd.DataFrame:
    """Generate missing-value statistics."""

    result = pd.DataFrame({
        "Entity": entity_name,
        "Column": df.columns,
        "Missing_Count": df.isna().sum().values,
        "Missing_Percentage": (
            df.isna().mean().values * 100
        ).round(2)
    })

    return result


# ---------------------------------------------------------
# Duplicate profile
# ---------------------------------------------------------

def profile_duplicates(
    df: pd.DataFrame,
    entity_name: str
) -> pd.DataFrame:
    """Generate duplicate-row statistics."""

    duplicate_count = int(df.duplicated().sum())

    result = pd.DataFrame([{
        "Entity": entity_name,
        "Total_Rows": len(df),
        "Duplicate_Rows": duplicate_count,
        "Duplicate_Percentage": round(
            duplicate_count / len(df) * 100, 2
        )
    }])

    return result


# ---------------------------------------------------------
# Numeric profile
# ---------------------------------------------------------

def profile_numeric_columns(
    df: pd.DataFrame,
    entity_name: str
) -> pd.DataFrame:
    """Generate descriptive statistics for numeric columns."""

    numeric_df = df.select_dtypes(include="number")

    if numeric_df.empty:
        return pd.DataFrame()

    profile = numeric_df.describe().T.reset_index()

    profile.rename(
        columns={"index": "Column"},
        inplace=True
    )

    profile.insert(0, "Entity", entity_name)

    return profile


# ---------------------------------------------------------
# Categorical profile
# ---------------------------------------------------------

def profile_categorical_columns(
    df: pd.DataFrame,
    entity_name: str
) -> pd.DataFrame:
    """Generate frequency profiles for categorical columns."""

    categorical_columns = df.select_dtypes(
        include=["object", "category"]
    ).columns

    records = []

    for column in categorical_columns:

        value_counts = (
            df[column]
            .value_counts(dropna=False)
        )

        for value, count in value_counts.items():

            percentage = round(
                count / len(df) * 100,
                2
            )

            records.append({
                "Entity": entity_name,
                "Column": column,
                "Value": value,
                "Count": count,
                "Percentage": percentage
            })

    return pd.DataFrame(records)


# ---------------------------------------------------------
# Profile one entity
# ---------------------------------------------------------

def profile_entity(
    df: pd.DataFrame,
    entity_name: str
) -> dict:
    """Run all profiling functions for one entity."""

    logger.info("Profiling entity: %s", entity_name)

    return {
        "columns": profile_columns(
            df,
            entity_name
        ),
        "missing": profile_missing_values(
            df,
            entity_name
        ),
        "duplicates": profile_duplicates(
            df,
            entity_name
        ),
        "numeric": profile_numeric_columns(
            df,
            entity_name
        ),
        "categorical": profile_categorical_columns(
            df,
            entity_name
        )
    }


# ---------------------------------------------------------
# Main profiling pipeline
# ---------------------------------------------------------

def main():

    logger.info("Starting raw-data profiling.")

    entities = {
        "customers": config["files"]["customers"],
        "products": config["files"]["products"],
        "stores": config["files"]["stores"],
        "orders": config["files"]["orders"]
    }

    all_columns = []
    all_missing = []
    all_duplicates = []
    all_numeric = []
    all_categorical = []

    for entity_name, file_name in entities.items():

        df = load_raw_data(file_name)

        results = profile_entity(
            df,
            entity_name
        )

        all_columns.append(results["columns"])
        all_missing.append(results["missing"])
        all_duplicates.append(results["duplicates"])

        if not results["numeric"].empty:
            all_numeric.append(results["numeric"])

        if not results["categorical"].empty:
            all_categorical.append(results["categorical"])

    # Combine reports

    pd.concat(
        all_columns,
        ignore_index=True
    ).to_csv(
        PROFILE_DIR / "column_profile.csv",
        index=False
    )

    pd.concat(
        all_missing,
        ignore_index=True
    ).to_csv(
        PROFILE_DIR / "missing_values.csv",
        index=False
    )

    pd.concat(
        all_duplicates,
        ignore_index=True
    ).to_csv(
        PROFILE_DIR / "duplicate_report.csv",
        index=False
    )

    if all_numeric:
        pd.concat(
            all_numeric,
            ignore_index=True
        ).to_csv(
            PROFILE_DIR / "numeric_profile.csv",
            index=False
        )

    if all_categorical:
        pd.concat(
            all_categorical,
            ignore_index=True
        ).to_csv(
            PROFILE_DIR / "category_profile.csv",
            index=False
        )

    logger.info(
        "Profiling completed successfully."
    )


if __name__ == "__main__":
    main()