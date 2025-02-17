#!/bin/bash

# Exit on error
set -e

# Variables
VENV_NAME="venv"
REQUIREMENTS_FILE="requirements.txt"
PROJECT_DIR="Network_App"
INVENTORY_SOURCE="./hosts-sample"
INVENTORY_DEST="./ansible/inventory/"

#!/bin/bash

# Check if Python3 is installed and get its version
PYTHON_VERSION=$(python3 --version 2>/dev/null | awk '{print $2}')
REQUIRED_VERSION="3.11"
PYTHON_EXEC="/usr/bin/python3.11"

# Function to install Python 3.11
install_python() {
    echo "Installing Python 3.11..."
    sudo $PACKAGE_MANAGER  update
    sudo $PACKAGE_MANAGER  install -y python3.11 
    echo "Python 3.11 installed successfully."
}

# Function to set Python 3.11 as the default
set_default_python() {
    echo "Setting Python 3.11 as the default..."
    sudo update-alternatives --install /usr/bin/python3 python3 $PYTHON_EXEC 1
    sudo update-alternatives --set python3 $PYTHON_EXEC
    echo "Python 3.11 is now the default."
}

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


# Check if Python 3.11 is installed
if [[ -x "$PYTHON_EXEC" ]]; then
    echo "Python 3.11 is already installed."
else
    echo "Python 3.11 is not installed. Installing..."
    install_python
fi

# Verify the current default Python version
PYTHON_MAJOR_MINOR=$(echo "$PYTHON_VERSION" | cut -d. -f1,2)

if [[ "$PYTHON_MAJOR_MINOR" != "$REQUIRED_VERSION" ]]; then
    echo "Updating default Python to 3.11..."
    set_default_python
else
    echo "Python 3.11 is already the default version."
fi

# Verify the update
python3 --version


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
