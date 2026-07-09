"""
This module contains the business and mathematical calculations for the
Vendor Payout & Deduction Engine. It supports both single-record processing
and high-volume bulk processing using vectorized Pandas operations.
"""

import pandas as pd
from models import PayoutRequest, PayoutResponse


def calculate_net_payout(request: PayoutRequest) -> PayoutResponse:
    """
    Calculates platform fees, variable taxes, and the final net payout for a vendor transaction.
    
    This function handles the core calculation logic. All monetary calculations
    are rounded to two decimal places to ensure precision.
    
    Args:
        request (PayoutRequest): The validation schema containing transaction details.
        
    Returns:
        PayoutResponse: The calculated payout details including individual deduction amounts.
    """
    # Calculate individual deduction amounts, rounded to 2 decimal places
    platform_fee_amount = round(request.gross_revenue * (request.platform_fee_percentage / 100.0), 2)
    tax_amount = round(request.gross_revenue * (request.variable_tax_percentage / 100.0), 2)
    
    # Calculate net payout by subtracting deductions from the gross revenue
    net_payout = round(request.gross_revenue - platform_fee_amount - tax_amount, 2)
    
    return PayoutResponse(
        transaction_id=request.transaction_id,
        vendor_id=request.vendor_id,
        gross_revenue=request.gross_revenue,
        platform_fee_amount=platform_fee_amount,
        tax_amount=tax_amount,
        net_payout=net_payout
    )


def process_bulk_csv(input_filepath: str, output_filepath: str) -> dict[str, str | int]:
    """
    Loads a CSV transaction dataset and computes vendor payouts using vectorized operations.
    
    Calculations for platform fees, tax amounts, and net payouts are executed concurrently 
    across the series arrays, avoiding standard python loops to preserve performance.
    
    Args:
        input_filepath (str): Path to the raw transactions CSV file.
        output_filepath (str): Path where the processed dataset will be exported.
        
    Returns:
        dict[str, str | int]: A processing summary including status and record count.
    """
    # Load dataset from file path
    df: pd.DataFrame = pd.read_csv(input_filepath)
    
    # Perform purely vectorized calculations, rounded to 2 decimal places
    df["platform_fee_amount"] = (df["gross_revenue"] * df["platform_fee_percentage"] / 100.0).round(2)
    df["tax_amount"] = (df["gross_revenue"] * df["variable_tax_percentage"] / 100.0).round(2)
    df["net_payout"] = (df["gross_revenue"] - df["platform_fee_amount"] - df["tax_amount"]).round(2)
    
    # Export fully processed file to local destination
    df.to_csv(output_filepath, index=False)
    
    return {
        "status": "success",
        "rows_processed": len(df),
        "file_saved": output_filepath
    }