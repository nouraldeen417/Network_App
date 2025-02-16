#!/bin/bash

# Define variables
PROJECT_DIR="./Storefront"
VENV_DIR="./venv"


# Check if the virtual environment exists
if [ ! -d "$VENV_DIR" ]; then
    echo "Error: Virtual environment not found. Please run setup.sh first."
    exit 1
fi

# Activate the virtual environment
echo "Activating the virtual environment..."
source "$VENV_DIR/bin/activate"


# Navigate to Django project directory
cd "$PROJECT_DIR"
echo "Starting Django application..."
python manage.py runserver 0.0.0.0:8000

echo "Django application is running at http://localhost:8000"

