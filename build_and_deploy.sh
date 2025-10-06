#!/bin/bash
# Deployment script for pysark100 to PyPI

set -e

echo "🔧 Installing build dependencies..."
pip install --upgrade build twine

echo "🧹 Cleaning previous builds..."
rm -rf build/ dist/ *.egg-info/

echo "📦 Building package..."
python -m build

echo "🔍 Checking package..."
python -m twine check dist/*

echo "✅ Package built successfully!"
echo ""
echo "📋 Next steps:"
echo "1. Test upload to TestPyPI:"
echo "   python -m twine upload --repository testpypi dist/*"
echo ""
echo "2. Install from TestPyPI to test:"
echo "   pip install --index-url https://test.pypi.org/simple/ pysark100"
echo ""
echo "3. Upload to PyPI (production):"
echo "   python -m twine upload dist/*"
echo ""
echo "📚 Files in dist/:"
ls -la dist/