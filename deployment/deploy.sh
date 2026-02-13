#!/bin/bash

# Set environment variables
export DB_HOST="localhost"
export DB_USER="username"
export DB_PASSWORD="password"
export DB_NAME="database_name"

# Build Docker image
echo "Building Docker image..."
docker build -t wifi-access-database .

# Start Docker container
echo "Starting Docker container..."
docker run -d --name wifi-access-db -e DB_HOST=$DB_HOST -e DB_USER=$DB_USER -e DB_PASSWORD=$DB_PASSWORD -e DB_NAME=$DB_NAME wifi-access-database

# Initialize the database
echo "Initializing database..."
docker exec wifi-access-db bash -c "mysql -h $DB_HOST -u $DB_USER -p$DB_PASSWORD -e 'CREATE DATABASE IF NOT EXISTS $DB_NAME;'"

# Run database migrations
echo "Running database migrations..."
docker exec wifi-access-db bash -c "npm run migrate"

echo "Deployment completed!"