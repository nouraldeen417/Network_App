#!/bin/bash

# Exit on error
set -e

# Variables
VENV_NAME="venv"
REQUIREMENTS_FILE="requirements.txt"
PROJECT_DIR="Network_App"
INVENTORY_SOURCE="./hosts-sample"
INVENTORY_DEST="./ansible/inventory/"

# go to project directory
cd $PROJECT_DIR

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null
then
    echo "Python 3 could not be found. Please install Python 3 and try again."
    exit 1
fi

# Detect package manager
if command -v apt &>/dev/null; then
    PACKAGE_MANAGER="apt"
elif command -v dnf &>/dev/null; then
    PACKAGE_MANAGER="dnf"
elif command -v yum &>/dev/null; then
    PACKAGE_MANAGER="yum"
else
    echo "Unsupported package manager. Install dependencies manually."
    exit 1
fi

# Create a virtual environment
echo "Creating virtual environment..."
python3 -m venv "$VENV_NAME"

# Activate the virtual environment
echo "Activating virtual environment..."
source "$VENV_NAME/bin/activate"

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install dependencies
if [ -f "$REQUIREMENTS_FILE" ]; then
    echo "Installing dependencies..."
    pip install -r "$REQUIREMENTS_FILE"
else
    echo "Requirements file not found. Skipping dependency installation."
fi

# Move the edited inventory file
echo "Moving the hosts file to $INVENTORY_DEST..."
sudo mv "$INVENTORY_SOURCE" "$INVENTORY_DEST"
sudo chmod 644 "$INVENTORY_DEST"
# Deactivate the virtual environment
echo "Deactivating virtual environment..."
deactivate

echo "Setup complete! Your environment is ready."
echo "To activate the virtual environment, run: source $VENV_NAME/bin/activate"
echo "To start the Django development server, run: python manage.py runserver"