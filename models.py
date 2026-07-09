"""
This module defines the Pydantic data models for the Vendor Payout & Deduction Engine.
It handles input validation, type enforcement, and documentation metadata.
"""

from pydantic import BaseModel, Field


class PayoutRequest(BaseModel):
    """
    Schema for validating incoming vendor payout requests.
    Enforces positive gross revenue and non-negative deduction percentages.
    """
    transaction_id: str = Field(
        ...,
        description="The unique identifier for the transaction being processed.",
        examples=["tx-100234"]
    )
    vendor_id: str = Field(
        ...,
        description="The anonymized unique identifier for the vendor.",
        examples=["v-8f72a"]
    )
    gross_revenue: float = Field(
        ...,
        gt=0,
        description="The raw transaction revenue before platform fees or taxes are applied. Must be strictly greater than zero.",
        examples=[1500.50]
    )
    platform_fee_percentage: float = Field(
        ...,
        ge=0,
        description="The percentage fee retained by the platform (e.g., 5.0 for 5%). Must be greater than or equal to zero.",
        examples=[5.0]
    )
    variable_tax_percentage: float = Field(
        ...,
        ge=0,
        description="The variable tax percentage to be deducted (e.g., 12.5 for 12.5%). Must be greater than or equal to zero.",
        examples=[12.5]
    )


class PayoutResponse(BaseModel):
    """
    Schema representing the processed response containing calculated payouts and deductions.
    """
    transaction_id: str = Field(
        ...,
        description="The unique identifier for the transaction processed.",
        examples=["tx-100234"]
    )
    vendor_id: str = Field(
        ...,
        description="The anonymized unique identifier for the vendor.",
        examples=["v-8f72a"]
    )
    gross_revenue: float = Field(
        ...,
        description="The raw transaction revenue before any deductions.",
        examples=[1500.50]
    )
    platform_fee_amount: float = Field(
        ...,
        description="The calculated platform fee amount, rounded to 2 decimal places.",
        examples=[75.03]
    )
    tax_amount: float = Field(
        ...,
        description="The calculated variable tax amount, rounded to 2 decimal places.",
        examples=[187.56]
    )
    net_payout: float = Field(
        ...,
        description="The final payout amount issued to the vendor after all deductions, rounded to 2 decimal places.",
        examples=[1237.91]
    )