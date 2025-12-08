#!/bin/bash
# Bootstrap script for Jayz Wayz development environment

set -e

echo "🚀 Bootstrapping Jayz Wayz development environment..."

# Check Python version
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: python3 is not installed"
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1,2)
REQUIRED_VERSION="3.9"

if [ "$(printf '%s\n' "$REQUIRED_VERSION" "$PYTHON_VERSION" | sort -V | head -n1)" != "$REQUIRED_VERSION" ]; then
    echo "❌ Error: Python $REQUIRED_VERSION or higher is required (found $PYTHON_VERSION)"
    exit 1
fi

echo "✓ Python version: $PYTHON_VERSION"

# Create virtual environment
if [ ! -d ".venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv .venv
else
    echo "✓ Virtual environment already exists"
fi

# Activate virtual environment
echo "🔌 Activating virtual environment..."
source .venv/bin/activate

# Upgrade pip
echo "⬆️  Upgrading pip..."
pip install --upgrade pip wheel setuptools

# Install package in development mode with dev dependencies
echo "📥 Installing package and dependencies..."
pip install -e ".[dev]"

echo ""
echo "✅ Bootstrap complete!"
echo ""
echo "To activate the environment, run:"
echo "  source .venv/bin/activate"
echo ""
echo "Then you can:"
echo "  - Run tests: pytest"
echo "  - Run demo: python -m jayz_wayz.orchestrator demo"
echo "  - List checkpoints: python -m jayz_wayz.orchestrator checkpoints list"
echo "  - Rollback: python -m jayz_wayz.orchestrator checkpoints rollback"
echo ""
