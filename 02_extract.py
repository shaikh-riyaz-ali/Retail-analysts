from pathlib import Path
import logging

import pandas as pd
import yaml


BASE_DIR = Path(__file__).resolve().parents[1]

CONFIG_PATH = BASE_DIR / "config" / "config.yaml"

with open(CONFIG_PATH, "r", encoding="utf-8") as file:
    config = yaml.safe_load(file)


RAW_DIR = BASE_DIR / config["paths"]["raw"]


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


def load_csv(file_name: str) -> pd.DataFrame:
    """Load a CSV file from the raw-data directory."""

    file_path = RAW_DIR / file_name

    if not file_path.exists():
        raise FileNotFoundError(
            f"Raw file not found: {file_path}"
        )

    logger.info("Loading: %s", file_path)

    df = pd.read_csv(file_path)

    logger.info(
        "Loaded %s rows x %s columns",
        len(df),
        len(df.columns)
    )

    return df


def extract_all() -> dict[str, pd.DataFrame]:
    """Extract all configured raw datasets."""

    entities = {
        "customers": config["files"]["customers"],
        "products": config["files"]["products"],
        "stores": config["files"]["stores"],
        "orders": config["files"]["orders"]
    }

    dataframes = {}

    for entity_name, file_name in entities.items():

        dataframes[entity_name] = load_csv(file_name)

    return dataframes


def main():

    logger.info("Starting extraction.")

    dataframes = extract_all()

    print("\nExtraction Summary")
    print("-" * 45)

    for entity_name, df in dataframes.items():

        print(
            f"{entity_name.title():10} : "
            f"{df.shape[0]:,} rows x "
            f"{df.shape[1]} columns"
        )

    logger.info("Extraction completed.")


if __name__ == "__main__":
    main()