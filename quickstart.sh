#!/bin/bash
# Quick Start Script for Hybrid Framework
# This script sets up and demonstrates the framework

echo "=================================================="
echo "🚀 HYBRID FRAMEWORK - QUICK START"
echo "=================================================="
echo ""

# Check Python version
echo "📋 Checking requirements..."
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "✅ Python version: $python_version"

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo ""
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
    echo "✅ Virtual environment created"
fi

# Activate virtual environment
echo ""
echo "🔌 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo ""
echo "📚 Installing dependencies..."
pip install -q --upgrade pip
pip install -q -r requirements.txt
echo "✅ Dependencies installed"

# Run demonstrations
echo ""
echo "=================================================="
echo "🎯 RUNNING DEMONSTRATIONS"
echo "=================================================="

# Demo 1: Agno Prototype
echo ""
echo "📝 Demo 1: Agno Rapid Prototype"
echo "--------------------------------------------------"
cd examples
python agno-prototype.py
cd ..

# Demo 2: Hybrid Bridge
echo ""
echo "🌉 Demo 2: Hybrid Bridge (Prototype → Production)"
echo "--------------------------------------------------"
cd examples
python hybrid-bridge.py
cd ..

echo ""
echo "=================================================="
echo "✨ QUICK START COMPLETE!"
echo "=================================================="
echo ""
echo "📖 Next Steps:"
echo "  1. Explore the examples/ directory"
echo "  2. Read the full documentation in README.md"
echo "  3. Check out agent-os-config.yaml for production configs"
echo "  4. Join our community Discord for support"
echo ""
echo "🚀 You're ready to build AI agents 10-20x faster!"
echo "=================================================="
