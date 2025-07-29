# Use official lightweight Python image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy source code
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Ensure the uploads/logs folder exists
RUN mkdir -p logs temp_uploads

# Set env var for Google credentials (used in .env too)
ENV GOOGLE_APPLICATION_CREDENTIALS=/app/google_credentials.json

# Expose FastAPI port
EXPOSE 8000

# Run FastAPI
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "9000"]
