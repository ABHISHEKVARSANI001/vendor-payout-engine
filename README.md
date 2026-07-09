# Vendor Payout & Deduction Engine

A high-performance, containerized RESTful microservice designed to automate variable vendor payout calculations, process bulk financial datasets, and forecast future revenue using Machine Learning.

##  Architecture Overview
This project is built as a modern, decoupled backend microservice. It is designed to handle enterprise-scale financial data pipeline tasks, avoiding traditional iterative loops in favor of vectorized calculations and deploying AI models via standard HTTP requests.

* **API Gateway:** Built with **FastAPI** for asynchronous request handling and automatic OpenAPI (Swagger) documentation.
* **Data Engineering:** Utilizes **Pandas** for pure vectorized array mathematics, capable of processing massive CSV batch uploads in milliseconds without blocking the main event loop.
* **Predictive Analytics:** Integrates a **Scikit-learn** `RandomForestRegressor` model to predict future vendor revenue trends based on historical transaction data.
* **DevOps & Containerization:** Fully containerized using **Docker** (`python:3.11-slim`) for guaranteed cross-platform consistency and rapid cloud deployment.

##  Tech Stack
* **Language:** Python 3.11
* **Framework:** FastAPI, Uvicorn
* **Data Manipulation:** Pandas, NumPy
* **Machine Learning:** Scikit-Learn, Joblib
* **Infrastructure:** Docker
* **Validation:** Pydantic

##  API Endpoints

### 1. Core Processing
* `GET /` - Microservice health check and status verification.
* `POST /calculate-payout` - Ingests a single vendor transaction, calculates platform fees and variable taxes, and returns the net payout.

### 2. Bulk Data Pipeline
* `POST /process-batch` - Accepts a raw `.csv` upload of 10,000+ transactions, executes vectorized Pandas calculations concurrently, and streams the fully processed `.csv` back to the client.

### 3. AI Inference
* `POST /predict-revenue` - Accepts current vendor financial metrics, transforms the payload into a 2D NumPy array, and runs it through the pre-trained Random Forest model to forecast the next month's gross revenue.

## Local Setup & Execution

The preferred method to run this microservice is via Docker, ensuring all ML dependencies and C-level binaries are perfectly isolated.

**1. Clone the repository:**
```bash
git clone https://github.com/ABHISHEKVARSANI001/vendor-payout-engine.git
cd vendor-payout-engine
```
**2. Build the Docker :**
```bash
docker build -t vendor-payout-engine .
```
**3. Run the Container:**
```bash
docker run -p 8000:8000 vendor-payout-engine
```
**4. Access the Dashboard:**
```bash
Navigate to http://127.0.0.1:8000/docs in your web browser to interact with the live Swagger UI and test the machine learning endpoints.
```

