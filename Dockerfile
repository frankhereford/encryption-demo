# Use the latest Python image from Docker Hub
FROM python:latest

# Set the working directory
WORKDIR /app

# Install phe library for Paillier encryption & others
RUN pip install phe requests phe qrcode brotli Pillow

# Copy the rest of your application code
COPY . /app/

# Run vote script when the container starts
CMD ["python", "2_voting.py"]
