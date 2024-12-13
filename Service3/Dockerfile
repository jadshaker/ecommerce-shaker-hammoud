# Base image
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Copy the application files
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port the app runs on
EXPOSE 5003  

# Command to run the application
CMD ["python", "app.py"]
