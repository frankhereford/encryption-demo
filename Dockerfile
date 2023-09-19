# Use the latest Python image from Docker Hub
FROM python:latest

# Set the working directory
WORKDIR /app

# Install phe library for Paillier encryption
RUN pip install phe

RUN pip install requests

# Copy the rest of your application code
COPY . /app/

# Run vote.py when the container starts
CMD ["python", "2_voting.py"]
