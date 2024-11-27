FROM python:3.9-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy service code and credentials
COPY spleeter_service.py .
COPY token.pickle .
COPY credentials/ ./credentials/

# Run service
CMD ["python", "spleeter_service.py"]