# Use a smaller base image
FROM python:3.8-slim

# Set working directory
WORKDIR /app

# Copy project files
COPY . /app

# Install dependencies (CPU-only PyTorch)
RUN pip install --no-cache-dir fastapi uvicorn transformers torch==2.0.1 --extra-index-url https://download.pytorch.org/whl/cpu boto3

# Expose the correct port
# Google Cloud Run expects 8080
EXPOSE 8080

# Use ENV variable to switch between development & production
ENV ENV=development
ENV LOCALHOST_ORIGIN="http://localhost:8000"
ENV REMOTEHOST_ORIGIN="https://your-frontend.github.io"

# Run FastAPI app
# Google cloud expects 8080
CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8080}"]
