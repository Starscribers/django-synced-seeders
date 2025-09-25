#!/bin/bash
# Serve documentation locally for development using uv and Sphinx

set -e

echo "🔧 Starting Django Synced Seeds documentation development server..."

# Check if uv is installed
if ! command -v uv &> /dev/null; then
    echo "❌ uv is not installed. Please install it first:"
    echo "   curl -LsSf https://astral.sh/uv/install.sh | sh"
    echo "   # or"
    echo "   pip install uv"
    exit 1
fi

# Install/sync documentation dependencies
echo "📦 Installing documentation dependencies..."
uv sync --group docs

# Build the documentation first
echo "� Building Sphinx documentation..."
uv run sphinx-build -b html docs site

# Serve the documentation
echo "🚀 Starting simple HTTP server..."
echo "📖 Documentation will be available at http://127.0.0.1:8000"
echo "🔄 Refresh your browser to see changes after rebuilding."
echo "Press Ctrl+C to stop the server."
cd site && python -m http.server 8000