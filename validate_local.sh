#!/bin/bash
set -e  # Exit immediately if a command exits with a non-zero status.

echo "🚀 Starting local validation..."

# Check and activate virtual environment
if [ -d ".venv" ]; then
    echo "🐍 Found .venv, activating..."
    source .venv/bin/activate
elif [ -d "venv" ]; then
    echo "🐍 Found venv, activating..."
    source venv/bin/activate
fi

# 1. Install Dependencies
echo "📦 Installing/Updating dependencies..."
python3 -m pip install --upgrade pip
python3 -m pip install setuptools wheel build black pylint pytest
if [ -f "setup.py" ]; then 
    echo "   Installing the package in editable mode..."
    python3 -m pip install .
fi

# 2. Check Formatting
echo "🎨 Checking formatting with Black..."
if ! black --check .; then
    echo "❌ Black formatting check failed. Run 'black .' to fix it."
    exit 1
fi

# 3. Linting
echo "🔍 Linting with Pylint..."
# Using the same flags as the GitHub Action
pylint AIFoundationKit --disable=C0114,C0115,C0116

# 4. Running Tests
echo "🧪 Running tests..."
pytest tests/

echo "✅ All validations passed! You are ready to push."
