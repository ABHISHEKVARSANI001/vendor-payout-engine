# Use the official lightweight Python 3.11 slim image as the base
FROM python:3.11-slim

# Set Python environment variables
# PYTHONDONTWRITEBYTECODE: Prevents creation of .pyc files inside the container
# PYTHONUNBUFFERED: Forces standard output/error to flush immediately, aiding log collection
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Establish the working directory inside the container filesystem
WORKDIR /app

# Copy only the dependencies file first to leverage Docker's layer cache
COPY requirements.txt .

# Install dependencies; --no-cache-dir prevents local package index storage, reducing overall image size
RUN pip install --no-cache-dir -U pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy all local source files (including local serialized model files) into the working directory
COPY . .

# Expose port 8000 to allow traffic transmission to the FastAPI process
EXPOSE 8000

# Instruct Docker to launch the Uvicorn ASGI server binding to all network interfaces on port 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]