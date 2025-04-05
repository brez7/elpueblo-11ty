# Use a lightweight Python base image
FROM python:3.11-slim

# Set the working directory
WORKDIR /app

# Copy your code into the container
COPY . /app

# Install dependencies
RUN pip install -r requirements.txt

# Start the server using gunicorn on port 8080
CMD ["gunicorn", "-b", "0.0.0.0:8080", "app:app"]

