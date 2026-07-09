"""
This module serves as the entry point for the Vendor Payout & Deduction Engine API.
It configures the FastAPI application instance, routes, and documentation settings.
"""

from fastapi import FastAPI
from models import PayoutRequest, PayoutResponse
from services import calculate_net_payout

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