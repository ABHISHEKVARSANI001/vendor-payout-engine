"""
This module serves as the entry point for the Vendor Payout & Deduction Engine API.
It configures the FastAPI application instance, routes, and documentation settings.
"""

from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse
from models import PayoutRequest, PayoutResponse
from services import calculate_net_payout, process_bulk_csv

# Initialize the FastAPI app with metadata for interactive documentation (Swagger UI / ReDoc)
app = FastAPI(
    title="Vendor Payout & Deduction Engine",
    description=(
        "A high-performance RESTful microservice designed to automate "
        "variable vendor payout calculations, platform fee deductions, "
        "and tax calculations at scale."
    ),
    version="1.0.0",
)


@app.get("/", tags=["Health Check"])
def health_check() -> dict[str, str]:
    """
    Verifies that the microservice is online and accessible.
    
    Returns:
        dict: A simple status dictionary indicating the service health status.
    """
    return {
        "status": "healthy",
        "service": "Vendor Payout & Deduction Engine"
    }


@app.post(
    "/calculate-payout",
    response_model=PayoutResponse,
    summary="Calculate Vendor Payout",
    tags=["Payouts"]
)
def calculate_payout(payload: PayoutRequest) -> PayoutResponse:
    """
    Calculates the net vendor payout for a transaction.
    
    This endpoint processes raw gross revenue, applies percentage-based platform fees 
    and variable tax rates, and returns the broken-down financial totals rounded to 
    two decimal places.
    
    Args:
        payload (PayoutRequest): The transaction detail containing revenue and deduction percentages.
        
    Returns:
        PayoutResponse: The calculated deduction amounts and final net vendor payout.
    """
    return calculate_net_payout(payload)


@app.post(
    "/process-batch",
    summary="Process Bulk Transactions CSV",
    tags=["Payouts"]
)
async def process_batch(file: UploadFile = File(...)) -> FileResponse:
    """
    Ingests a CSV transaction dataset, applies fee and tax calculations in bulk, 
    and returns a fully calculated CSV dataset.
    
    The input CSV must map columns directly to schema parameters:
    (transaction_id, vendor_id, gross_revenue, platform_fee_percentage, variable_tax_percentage)
    
    Args:
        file (UploadFile): The raw uploaded CSV file containing transactions.
        
    Returns:
        FileResponse: A downloadable CSV containing original columns augmented with 
        platform_fee_amount, tax_amount, and net_payout columns.
    """
    input_temp_path = "temp_upload.csv"
    output_temp_path = "temp_processed.csv"
    
    # Safely save the uploaded file streaming contents to the local disk
    with open(input_temp_path, "wb") as buffer:
        content = await file.read()
        buffer.write(content)
        
    # Execute the high-volume vectorized Pandas engine
    process_bulk_csv(input_temp_path, output_temp_path)
    
    # Return the processed file as a downloadable attachment
    return FileResponse(
        path=output_temp_path,
        media_type="text/csv",
        filename="processed_payouts.csv"
    )