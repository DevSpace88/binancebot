FROM python:3.12-alpine

WORKDIR /app

# Install system dependencies using Alpine's package manager (apk)
RUN apk add --no-cache \
    build-base \
    gcc

# Copy requirements file
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create necessary directories
RUN mkdir -p data logs models

# Expose port
EXPOSE 8000

# Run the application
CMD ["python", "start.py", "--port", "8000"]