import pandas as pd
import logging
import os
from typing import List, Dict

# Configure logging to look like a professional monitoring tool
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - [DATA QUALITY] - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

class DataValidator:
    """
    Automated Data Validation Suite
    --------------------------------
    Ensures data integrity, schema compliance, and logical consistency 
    before data is loaded into the Data Warehouse.
    """

    def __init__(self, df: pd.DataFrame, dataset_name: str):
        self.df = df
        self.name = dataset_name
        self.errors = []

    def validate_schema(self, required_columns: List[str]) -> bool:
        """Checks if all critical columns exist in the dataset."""
        missing = [col for col in required_columns if col not in self.df.columns]
        if missing:
            msg = f"SCHEMA MISMATCH in {self.name}: Missing columns {missing}"
            logger.error(msg)
            self.errors.append(msg)
            return False
        logger.info(f"Schema check passed for {self.name}.")
        return True

    def check_nulls(self, critical_columns: List[str]):
        """Alerts on null values in fields that must not be empty."""
        for col in critical_columns:
            if col in self.df.columns:
                null_count = self.df[col].isnull().sum()
                if null_count > 0:
                    msg = f"DATA QUALITY ALERT: Found {null_count} NULLs in {self.name} column '{col}'"
                    logger.warning(msg) # Warning, not critical error
        logger.info(f"Null value check complete for {self.name}.")

    def validate_logical_rules(self):
        """Performs domain-specific integrity checks."""
        # Rule 1: Popularity must be between 0 and 100
        if 'popularity' in self.df.columns:
            invalid_pop = self.df[(self.df['popularity'] < 0) | (self.df['popularity'] > 100)]
            if not invalid_pop.empty:
                logger.error(f"INTEGRITY ERROR: {len(invalid_pop)} records with invalid popularity in {self.name}")

        # Rule 2: Duration must be positive
        if 'duration_ms' in self.df.columns:
            invalid_dur = self.df[self.df['duration_ms'] <= 0]
            if not invalid_dur.empty:
                logger.error(f"INTEGRITY ERROR: {len(invalid_dur)} tracks with 0 or negative duration in {self.name}")

        # Rule 3: Followers cannot be negative
        if 'followers' in self.df.columns:
            invalid_fol = self.df[self.df['followers'] < 0]
            if not invalid_fol.empty:
                logger.error(f"INTEGRITY ERROR: Negative follower counts detected in {self.name}")

    def check_uniqueness(self, primary_keys: List[str]):
        """Ensures idempotency by checking for duplicates on primary keys."""
        if set(primary_keys).issubset(self.df.columns):
            duplicates = self.df.duplicated(subset=primary_keys).sum()
            if duplicates > 0:
                logger.warning(f"DUPLICATE ALERT: Found {duplicates} duplicate records in {self.name} based on keys {primary_keys}")
            else:
                logger.info(f"Uniqueness check passed for {self.name}.")

def run_validation():
    base_path = os.getenv("AIRFLOW_HOME", os.getcwd())
    
    # Define expectations for each dataset
    configs = [
        {
            "file": "cleaned_artist_streams.csv",
            "name": "Artists Data",
            "schema": ["artist_id", "artist_name", "popularity", "followers"],
            "keys": ["artist_id"]
        },
        {
            "file": "cleaned_playlists.csv",
            "name": "Playlists Data",
            "schema": ["playlist_id", "playlist_name", "total_tracks"],
            "keys": ["playlist_id"]
        },
        {
            "file": "cleaned_playlists_tracks_streams.csv",
            "name": "Tracks Data",
            "schema": ["playlist_id", "track_id", "track_name", "duration_ms"],
            "keys": ["playlist_id", "track_id"]
        }
    ]

    print("\n" + "="*50)
    print("STARTING AUTOMATED DATA VALIDATION SUITE")
    print("="*50)

    for config in configs:
        file_path = os.path.join(base_path, config["file"])
        
        if not os.path.exists(file_path):
            logger.warning(f"Skipping {config['name']}: File not found at {file_path}")
            continue

        try:
            # Validate the CSV
            df = pd.read_csv(file_path)
            validator = DataValidator(df, config["name"])
            
            validator.validate_schema(config["schema"])
            validator.check_nulls(config["schema"])
            validator.validate_logical_rules()
            validator.check_uniqueness(config["keys"])
            
        except Exception as e:
            logger.critical(f"Validation crashed for {config['name']}: {str(e)}")

    print("="*50 + "\n")

if __name__ == "__main__":
    run_validation()