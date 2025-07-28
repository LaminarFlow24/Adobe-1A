# Use a lightweight Python image
FROM python:3.9-slim

# Set work directory to /app (where our scripts live)
WORKDIR /app

# Install system dependencies (for PDF processing)
RUN apt-get update && apt-get install -y \
    poppler-utils \
    && rm -rf /var/lib/apt/lists/*

# Copy the application code into the container
COPY app/ /app/

# Install Python dependencies (ignore if no requirements.txt)
RUN pip install --no-cache-dir -r requirements.txt || true

# Ensure input/output directories exist
RUN mkdir -p /app/input /app/output

# Set default command to run the test runner
CMD ["python3", "test_runner.py"]
