"""
This module serves as the entry point for the Vendor Payout & Deduction Engine API.
It configures the FastAPI application instance, routes, and documentation settings.
"""

import joblib
import numpy as np
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
from models import PayoutRequest, PayoutResponse, PredictionRequest, PredictionResponse
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

# Load the machine learning model on application startup
MODEL_PATH = "revenue_predictor.joblib"
try:
    predictor_model = joblib.load(MODEL_PATH)
except FileNotFoundError:
    predictor_model = None
    # Log the warning to console; allows backend to function without crashing if model is missing
    print(f"Warning: Model file '{MODEL_PATH}' was not found. Prediction endpoint will return a 503 error until configured.")


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


@app.post(
    "/predict-revenue",
    response_model=PredictionResponse,
    summary="Predict Next Month's Vendor Revenue",
    tags=["Predictive Analytics"]
)
def predict_revenue(payload: PredictionRequest) -> PredictionResponse:
    """
    Infers next month's predicted revenue for a vendor utilizing a trained machine learning model.
    
    Takes standard financial features and formats them into a 2D matrix structure to execute
    inference through a serialized RandomForestRegressor pipeline.
    
    Args:
        payload (PredictionRequest): Validation schema wrapper containing feature variables.
        
    Returns:
        PredictionResponse: A predicted revenue estimate, rounded to 2 decimal places.
        
    Raises:
        HTTPException: 503 error if the underlying estimator object is uninitialized or missing.
    """
    if predictor_model is None:
        raise HTTPException(
            status_code=503,
            detail="Predictive analysis model is currently uninitialized or unavailable on server."
        )

    # Scikit-learn estimators require a 2D array representation for feature matrix data
    features_array = np.array([[
        payload.gross_revenue,
        payload.platform_fee_percentage,
        payload.variable_tax_percentage
    ]])

    # Generate inference values and parse the result
    model_prediction = predictor_model.predict(features_array)
    predicted_value: float = round(float(model_prediction[0]), 2)

    return PredictionResponse(predicted_next_month_revenue=predicted_value)