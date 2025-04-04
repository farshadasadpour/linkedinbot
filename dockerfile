FROM python:3.12.9-alpine

WORKDIR /app

# Install system dependencies for Selenium & WebDriver support
RUN pip install --no-cache-dir --upgrade pip

# Copy application files
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Set a non-root user for security
USER 1001

# Run the script
CMD ["python3", "main.py"]
