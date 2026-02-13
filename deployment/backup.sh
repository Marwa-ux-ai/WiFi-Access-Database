#!/bin/bash

# This script creates a backup of the PostgreSQL database, compresses it, and cleans up old backups.

# Database credentials
USER="your_username"
PASSWORD="your_password"
HOST="localhost"
DB_NAME="your_database"

# Backup Directory
BACKUP_DIR="/path/to/backup/directory"

# Date format for the backup filename
DATE=$(date +'%Y-%m-%d_%H-%M-%S')

# Number of days to keep backups
DAYS_TO_KEEP=7

# Create Backup
echo "Creating backup..."
pg_dump -U $USER -h $HOST $DB_NAME | gzip > $BACKUP_DIR/backup_$DATE.sql.gz

if [ $? -eq 0 ]; then
    echo "Backup created successfully: $BACKUP_DIR/backup_$DATE.sql.gz"
else
    echo "Error creating backup"
    exit 1
fi

# Cleanup old backups
find $BACKUP_DIR -type f -name "backup_*.sql.gz" -mtime +$DAYS_TO_KEEP -exec rm {} \;

echo "Old backups cleaned up successfully."