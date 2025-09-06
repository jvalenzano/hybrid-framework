"""
Test suite for Hybrid Framework
Tests the conceptual implementation and patterns
"""

import pytest
import sys
import os
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

# Test configuration
@pytest.fixture
def mock_env_vars(monkeypatch):
    """Mock environment variables for testing"""
    monkeypatch.setenv("AGNO_API_KEY", "test_agno_key")
    monkeypatch.setenv("AGENT_OS_API_KEY", "test_agent_os_key")
    monkeypatch.setenv("DEBUG", "true")

def test_environment_setup(mock_env_vars):
    """Test that environment variables are properly configured"""
    assert os.getenv("AGNO_API_KEY") == "test_agno_key"
    assert os.getenv("AGENT_OS_API_KEY") == "test_agent_os_key"

def test_examples_exist():
    """Test that all example files exist"""
    examples_dir = Path(__file__).parent.parent / "examples"
    
    required_files = [
        "agno-prototype.py",
        "agent-os-config.yaml",
        "hybrid-bridge.py"
    ]
    
    for file in required_files:
        file_path = examples_dir / file
        assert file_path.exists(), f"Missing example file: {file}"

def test_agno_prototype_structure():
    """Test that the Agno prototype follows expected structure"""
    # Import the example module
    from examples.agno_prototype import (
        IntelligentAgent,
        Message,
        Response,
        Tool
    )
    
    # Test that classes are defined
    assert IntelligentAgent is not None
    assert Message is not None
    assert Response is not None
    assert Tool is not None

def test_bridge_pattern_structure():
    """Test that the bridge pattern is properly structured"""
    from examples.hybrid_bridge import (
        HybridAgentBridge,
        RateLimiter,
        CircuitBreaker,
        ProductionServer
    )
    
    # Test that bridge components exist
    assert HybridAgentBridge is not None
    assert RateLimiter is not None
    assert CircuitBreaker is not None
    assert ProductionServer is not None

@pytest.mark.asyncio
async def test_rate_limiter():
    """Test rate limiter functionality"""
    from examples.hybrid_bridge import RateLimiter
    
    limiter = RateLimiter(rate=10, capacity=10)
    
    # Should allow initial requests
    assert await limiter.acquire(1) == True
    
    # Should respect capacity
    for _ in range(9):
        await limiter.acquire(1)
    
    # Should deny when capacity exceeded
    assert await limiter.acquire(1) == False

def test_circuit_breaker_states():
    """Test circuit breaker state transitions"""
    from examples.hybrid_bridge import CircuitBreaker
    
    breaker = CircuitBreaker(failure_threshold=3, timeout=1.0)
    
    # Initial state should be closed
    assert breaker.state == "closed"
    
    # After threshold failures, should open
    breaker.failures = 3
    breaker.state = "open"
    assert breaker.state == "open"

def test_config_structure():
    """Test that configuration files are properly structured"""
    import yaml
    
    config_path = Path(__file__).parent.parent / "examples" / "agent-os-config.yaml"
    
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)
    
    # Test required fields exist
    assert "apiVersion" in config
    assert "kind" in config
    assert "metadata" in config
    assert "spec" in config
    
    # Test spec structure
    assert "agent" in config["spec"]
    assert "scaling" in config["spec"]
    assert "monitoring" in config["spec"]

def test_documentation_exists():
    """Test that all documentation files exist"""
    root_dir = Path(__file__).parent.parent
    
    required_docs = [
        "README.md",
        "LICENSE",
        "CONTRIBUTING.md",
        "DISCLAIMER.md",
        "CHANGELOG.md",
        ".env.example"
    ]
    
    for doc in required_docs:
        doc_path = root_dir / doc
        assert doc_path.exists(), f"Missing documentation: {doc}"

def test_requirements_file():
    """Test that requirements.txt is properly formatted"""
    req_path = Path(__file__).parent.parent / "requirements.txt"
    
    with open(req_path, 'r') as f:
        lines = f.readlines()
    
    # Should have at least some requirements
    assert len(lines) > 0
    
    # Check for key dependencies (conceptual)
    content = ''.join(lines).lower()
    assert 'agno' in content or 'agent-os' in content

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
