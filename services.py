"""
This module contains the business and mathematical calculations for the
Vendor Payout & Deduction Engine.
"""

from models import PayoutRequest, PayoutResponse


def calculate_net_payout(request: PayoutRequest) -> PayoutResponse:
    """
    Calculates platform fees, taxes, and the final net payout for a vendor transaction.
    
    All calculations are rounded to 2 decimal places to ensure consistent precision 
    with financial standard formatting.
    
    Args:
        request (PayoutRequest): Validated transaction and deduction rate data.
        
    Returns:
        PayoutResponse: The calculated fees, taxes, and net payout matching the response schema.
    """
    # Calculate percentage-based deductions rounded to 2 decimal places
    platform_fee_amount: float = round(
        request.gross_revenue * (request.platform_fee_percentage / 100.0), 2
    )
    tax_amount: float = round(
        request.gross_revenue * (request.variable_tax_percentage / 100.0), 2
    )
    
    # Calculate final net payout after deductions, rounded to 2 decimal places
    net_payout: float = round(
        request.gross_revenue - platform_fee_amount - tax_amount, 2
    )
    
    return PayoutResponse(
        transaction_id=request.transaction_id,
        vendor_id=request.vendor_id,
        gross_revenue=request.gross_revenue,
        platform_fee_amount=platform_fee_amount,
        tax_amount=tax_amount,
        net_payout=net_payout
    )