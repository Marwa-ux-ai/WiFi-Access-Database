# Dockerfile

# Use the official Python 3.11 base image
FROM python:3.11

# Set the working directory in the container
WORKDIR /app

# Copy the requirements.txt file to the container
COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code to the container
COPY . .

# Set the environment variable for the application
ENV PYTHONUNBUFFERED=1

# Expose the port the app runs on
EXPOSE 5000

# Health check command
HEALTHCHECK CMD curl --fail http://localhost:5000/health || exit 1

# Run the application
CMD ["python", "app.py"]