#!/usr/bin/env bash
set -euo pipefail

# marketing-agent — First-time setup
# Usage: ./setup.sh

echo "=== marketing-agent Setup ==="
echo ""

# Check for Python 3
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is required but not installed."
    echo "Visit https://www.python.org/downloads/ or use your package manager."
    exit 1
fi

PYTHON_VERSION=$(python3 --version | awk '{print $2}')
echo "Python version: $PYTHON_VERSION"
echo ""

# Install Python dependencies
echo "Installing Python dependencies..."
pip install -r data_sources/requirements.txt
echo "✓ Dependencies installed"
echo ""

# Create .env files if they don't exist
if [ ! -f .env ]; then
    echo "Creating .env from template..."
    cp .env.example .env
    echo "✓ Created .env"
else
    echo "✓ .env already exists"
fi

if [ ! -f data_sources/config/.env ]; then
    echo "Creating data_sources/config/.env from template..."
    cp data_sources/config/.env.example data_sources/config/.env
    echo "✓ Created data_sources/config/.env"
else
    echo "✓ data_sources/config/.env already exists"
fi

echo ""
echo "=== Setup complete! ==="
echo ""
echo "Next steps:"
echo "  1. Open this directory in Claude Code:"
echo "     claude ."
echo "  2. Run /setup in Claude Code to configure your brand voice and content strategy"
echo "  3. (Optional) Edit .env and data_sources/config/.env with API credentials"
echo "  4. Start creating content:"
echo "     /write [topic]"
echo ""
echo "For more info, see README.md"
