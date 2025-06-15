#!/bin/bash

# Define variables
PROJECT_DIR="Network_App"
VENV_DIR="./venv"


# Navigate to Django project directory# Check if the virtual environment exists
if [ ! -d "$VENV_DIR" ]; then
    echo "Error: Virtual environment not found. Please run setup.sh first."
    exit 1
fi

# Activate the virtual environment
echo "Activating the virtual environment..."
source "$VENV_DIR/bin/activate"


# Start the Django development server
echo "Starting Django application..."
python manage.py runserver 0.0.0.0:8000 

echo "Django application is running at http://localhost:8000"

