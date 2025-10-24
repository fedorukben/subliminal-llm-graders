#!/bin/bash
# Setup script for Academic Integrity Detection Experiment

echo "========================================"
echo "Academic Integrity Detection Setup"
echo "========================================"
echo ""

# Check Python version
echo "Checking Python version..."
python_version=$(python3 --version 2>&1 | grep -oP '\d+\.\d+' | head -1)
required_version="3.8"

if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" != "$required_version" ]; then
    echo "ERROR: Python 3.8+ required. Found: $python_version"
    exit 1
fi
echo "✓ Python $python_version found"

# Create virtual environment
echo ""
echo "Creating virtual environment..."
python3 -m venv venv
echo "✓ Virtual environment created"

# Activate virtual environment
echo ""
echo "Activating virtual environment..."
source venv/bin/activate
echo "✓ Virtual environment activated"

# Upgrade pip
echo ""
echo "Upgrading pip..."
pip install --upgrade pip > /dev/null 2>&1
echo "✓ Pip upgraded"

# Install requirements
echo ""
echo "Installing dependencies..."
pip install -r requirements.txt
echo "✓ Dependencies installed"

# Create directories
echo ""
echo "Creating directory structure..."
mkdir -p results
mkdir -p logs
mkdir -p config
mkdir -p utils
echo "✓ Directories created"

# Setup .env file
echo ""
if [ ! -f .env ]; then
    echo "Creating .env file from template..."
    cp .env.example .env
    echo "✓ .env file created"
    echo ""
    echo "⚠️  IMPORTANT: Edit .env file and add your API keys!"
    echo "   Required: OPENAI_API_KEY, ANTHROPIC_API_KEY, GOOGLE_API_KEY"
else
    echo ".env file already exists"
fi

# Make scripts executable
echo ""
echo "Making scripts executable..."
chmod +x run_experiment.py
chmod +x utils/analyze_results.py
chmod +x setup.sh
echo "✓ Scripts are executable"

echo ""
echo "========================================"
echo "Setup Complete!"
echo "========================================"
echo ""
echo "Next steps:"
echo "1. Edit .env and add your API keys"
echo "2. Activate the virtual environment:"
echo "   source venv/bin/activate"
echo "3. Run a quick test:"
echo "   python run_experiment.py --quick-test"
echo "4. Run the full experiment:"
echo "   python run_experiment.py"
echo ""
