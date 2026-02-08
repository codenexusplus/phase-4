FROM python:3.11-slim
WORKDIR /app

# Install system dependencies required for bcrypt and other packages
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    musl-dev \
    libffi-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first to leverage Docker cache
COPY requirements.txt .
# Install bcrypt and passlib first with specific versions to ensure compatibility
RUN pip install --no-cache-dir "bcrypt==4.0.1" "passlib[bcrypt]==1.7.4"
# Then install the rest of the requirements
RUN pip install --no-cache-dir --default-timeout=100 -r requirements.txt

# Copy the rest of the application
COPY . .

ENV PYTHONPATH=/app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
