import time
from services import process_bulk_csv

print("Starting batch processing job...")

# Start the stopwatch
start_time = time.time()

# Run the engine
result = process_bulk_csv("mock_transactions.csv", "processed_transactions.csv")

# Stop the stopwatch
end_time = time.time()
time_taken = end_time - start_time

print(f"\nJob Summary: {result}")
print(f"Processing Speed: {time_taken:.5f} seconds")