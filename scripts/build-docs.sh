#!/bin/bash
# Build documentation using uv and Sphinx for faster dependency installation

set -e

echo "🔧 Building Django Synced Seeds documentation with uv and Sphinx..."

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

# Build the documentation
echo "📚 Building Sphinx documentation..."
uv run sphinx-build -b html docs site

echo "✅ Documentation built successfully!"
echo "📖 Open site/index.html in your browser to view the documentation."
echo "🚀 Or run './scripts/serve-docs.sh' to start a development server."
