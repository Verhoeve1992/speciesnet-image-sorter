#!/bin/bash
# Quick start script for Simple Image Sorter

echo "🖼️  Simple Image Sorter - Quick Start"
echo "====================================="
echo ""

# Check Python version
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "Python version: $python_version"

# Check if pip is available
if ! command -v pip &> /dev/null; then
    echo "❌ pip not found. Please install Python 3.10 or higher."
    exit 1
fi

echo ""
echo "Choose how to run the app:"
echo "1. Desktop app (PyQt6)"
echo "2. Web app (Streamlit)"
echo ""
read -p "Enter your choice (1 or 2): " choice

case $choice in
    1)
        echo ""
        echo "📦 Installing desktop dependencies..."
        pip install -e ".[desktop]"
        
        echo ""
        echo "🚀 Starting desktop app..."
        python main.py
        ;;
    2)
        echo ""
        echo "📦 Installing web app dependencies..."
        pip install -e ".[streamlit]"
        
        echo ""
        echo "🚀 Starting web app..."
        echo "The app will open in your browser at http://localhost:8501"
        streamlit run streamlit_main.py
        ;;
    *)
        echo "❌ Invalid choice. Please enter 1 or 2."
        exit 1
        ;;
esac
