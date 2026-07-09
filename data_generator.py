"""
This script generates mock transaction dataset for the Vendor Payout & Deduction Engine.
It creates a CSV file containing 10,000 records structured to match the API ingestion schema.
"""

import numpy as np
import pandas as pd


def generate_mock_data(output_filepath: str = "mock_transactions.csv") -> None:
    """
    Generates a 10,000-row dataset of mock transactions and writes it to a CSV file.
    
    The dataset includes transactional identifiers, vendor IDs, gross revenues,
    and platform/tax percentage fields conforming to the Pydantic ingestion constraints.
    
    Args:
        output_filepath (str): The destination path for the generated CSV file.
    """
    # Set seed for reproducibility of random generations
    np.random.seed(42)
    num_records = 10000

    # 1. Generate unique sequential transaction IDs
    transaction_ids = [f"TXN-{i:05d}" for i in range(10001, 10001 + num_records)]

    # 2. Define a pool of 50 unique vendor IDs and randomly sample with replacement
    vendor_pool = [f"VND-{i:02d}" for i in range(1, 51)]
    vendor_ids = np.random.choice(vendor_pool, size=num_records)

    # 3. Generate random float gross revenues between 50.00 and 5000.00 rounded to 2 decimal places
    gross_revenues = np.round(np.random.uniform(50.00, 5000.00, size=num_records), 2)

    # 4. Randomly assign percentage-based platform fees and tax options
    fee_options = [2.5, 5.0, 7.5]
    tax_options = [10.0, 15.0, 20.0]
    
    platform_fee_percentages = np.random.choice(fee_options, size=num_records)
    variable_tax_percentages = np.random.choice(tax_options, size=num_records)

    # Construct the Pandas DataFrame
    df = pd.DataFrame({
        "transaction_id": transaction_ids,
        "vendor_id": vendor_ids,
        "gross_revenue": gross_revenues,
        "platform_fee_percentage": platform_fee_percentages,
        "variable_tax_percentage": variable_tax_percentages
    })

    # Export to CSV without the default DataFrame index
    df.to_csv(output_filepath, index=False)
    
    print(f"Successfully generated and saved {num_records} records to '{output_filepath}'.")
    print("\nFirst 5 rows of the generated dataset:")
    print(df.head())


if __name__ == "__main__":
    generate_mock_data()