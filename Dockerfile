# Use a valid lightweight Python image
FROM python:3.12-slim

# Set the working directory inside the container
WORKDIR /app

# Install system dependencies first
RUN apt update -y && \
    apt install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY . .

# Explicitly expose the correct port (matches Streamlit port)
EXPOSE 8051

# Proper Streamlit command with headless mode
CMD ["streamlit", "run", "app.py", \
    "--server.port=8051", \
    "--server.address=0.0.0.0", \
    "--server.headless=true", \
    "--browser.serverAddress=0.0.0.0", \
    "--browser.gatherUsageStats=False"]