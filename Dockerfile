# Use a smaller base image
FROM python:3.8-slim

# Install Git and Git LFS (needed for runtime LFS support)
RUN apt-get update && apt-get install -y git git-lfs
RUN git lfs install

# Set working directory
WORKDIR /app

# Copy project files (LFS files should already be present)
COPY . /app

# Install dependencies (CPU-only PyTorch)
RUN pip install --no-cache-dir fastapi uvicorn transformers torch==2.0.1 --extra-index-url https://download.pytorch.org/whl/cpu boto3

# Expose the correct port
EXPOSE 8080

# Debug: List contents of model directory
RUN ls -lh /app/model || echo "Model directory is empty!"

# Run FastAPI app
CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8080}"]
