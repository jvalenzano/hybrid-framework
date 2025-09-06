#!/usr/bin/env python3
"""
Test script to verify the Hybrid Framework installation
Run this to ensure everything is working correctly
"""

import sys
import importlib
import subprocess
from pathlib import Path

def check_python_version():
    """Check if Python version meets requirements"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print(f"❌ Python 3.8+ required, found {version.major}.{version.minor}")
        return False
    print(f"✅ Python version: {version.major}.{version.minor}.{version.micro}")
    return True

def check_import(module_name):
    """Check if a module can be imported"""
    try:
        importlib.import_module(module_name)
        print(f"✅ {module_name} installed")
        return True
    except ImportError:
        print(f"❌ {module_name} not found")
        return False

def check_examples():
    """Check if example files exist"""
    examples_dir = Path("examples")
    required_files = [
        "agno-prototype.py",
        "agent-os-config.yaml",
        "hybrid-bridge.py"
    ]
    
    all_exist = True
    for file in required_files:
        path = examples_dir / file
        if path.exists():
            print(f"✅ {file} found")
        else:
            print(f"❌ {file} missing")
            all_exist = False
    
    return all_exist

def run_simple_test():
    """Run a simple test of the Agno prototype"""
    try:
        # Change to examples directory
        import os
        os.chdir("examples")
        
        # Import and test the agent
        from agno_prototype import IntelligentAgent, Message
        from datetime import datetime
        import asyncio
        
        async def test():
            agent = IntelligentAgent("test-agent")
            message = Message(
                content="Hello, can you help me?",
                timestamp=datetime.now(),
                user_id="test-user"
            )
            response = await agent.execute(message)
            return response.success
        
        result = asyncio.run(test())
        os.chdir("..")
        
        if result:
            print("✅ Agent test successful")
            return True
        else:
            print("❌ Agent test failed")
            return False
            
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

def main():
    """Main test function"""
    print("="*60)
    print("🔍 HYBRID FRAMEWORK - INSTALLATION TEST")
    print("="*60)
    print()
    
    all_passed = True
    
    # Check Python version
    print("📋 Checking Python version...")
    if not check_python_version():
        all_passed = False
    print()
    
    # Check required packages
    print("📦 Checking core dependencies...")
    core_packages = ["asyncio", "dataclasses", "typing", "json"]
    for package in core_packages:
        if not check_import(package):
            all_passed = False
    print()
    
    # Check example files
    print("📁 Checking example files...")
    if not check_examples():
        all_passed = False
    print()
    
    # Run simple test
    print("🧪 Running simple agent test...")
    if not run_simple_test():
        all_passed = False
    print()
    
    # Results
    print("="*60)
    if all_passed:
        print("✨ ALL TESTS PASSED!")
        print("Your Hybrid Framework installation is ready to use.")
        print()
        print("Next steps:")
        print("  1. Run ./quickstart.sh for full demonstration")
        print("  2. Explore the examples/ directory")
        print("  3. Read the README.md for documentation")
    else:
        print("⚠️ SOME TESTS FAILED")
        print("Please install missing dependencies:")
        print("  pip install -r requirements.txt")
    print("="*60)

if __name__ == "__main__":
    main()
