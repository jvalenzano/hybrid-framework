# Contributing to Hybrid Framework

First off, thank you for considering contributing to the Hybrid Framework! It's people like you that make this framework a great tool for the AI development community.

## Code of Conduct

By participating in this project, you are expected to uphold our Code of Conduct:
- Be respectful and inclusive
- Welcome newcomers and help them get started
- Focus on constructive criticism
- Show empathy towards other community members

## How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check existing issues to avoid duplicates. When you create a bug report, include as many details as possible:

- **Use a clear and descriptive title**
- **Describe the exact steps to reproduce the problem**
- **Provide specific examples**
- **Describe the behavior you observed and expected**
- **Include screenshots if relevant**
- **Include your environment details** (OS, Python version, etc.)

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion:

- **Use a clear and descriptive title**
- **Provide a detailed description of the proposed enhancement**
- **Explain why this enhancement would be useful**
- **List any alternative solutions you've considered**

### Pull Requests

1. **Fork the repository** and create your branch from `main`
2. **Follow the coding standards** (see below)
3. **Write tests** for your changes
4. **Ensure all tests pass**
5. **Update documentation** as needed
6. **Submit a pull request**

## Development Setup

1. Clone your fork:
```bash
git clone https://github.com/your-username/hybrid-framework.git
cd hybrid-framework
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
pip install -r requirements-dev.txt  # Development dependencies
```

4. Set up pre-commit hooks:
```bash
pre-commit install
```

## Coding Standards

### Python Style Guide

We follow PEP 8 with some modifications:
- Line length: 88 characters (Black default)
- Use type hints for all function signatures
- Write docstrings for all public functions and classes

### Code Formatting

We use automated formatting tools:
```bash
# Format code with Black
black .

# Sort imports with isort
isort .

# Check code with ruff
ruff check .

# Type checking with mypy
mypy .
```

### Commit Messages

Follow the [Conventional Commits](https://www.conventionalcommits.org/) specification:

- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation changes
- `style:` Code style changes (formatting, etc.)
- `refactor:` Code refactoring
- `test:` Test additions or modifications
- `chore:` Maintenance tasks

Example:
```
feat: add support for custom Agent OS configurations

- Added configuration validator
- Implemented YAML schema validation
- Updated documentation with examples
```

## Testing

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=.

# Run specific test file
pytest tests/test_agno_prototype.py

# Run with verbose output
pytest -v
```

### Writing Tests

- Place tests in the `tests/` directory
- Mirror the source code structure
- Use descriptive test names
- Include both positive and negative test cases
- Aim for >80% code coverage

Example test:
```python
import pytest
from examples.agno_prototype import IntelligentAgent, Message

@pytest.mark.asyncio
async def test_agent_initialization():
    """Test that agent initializes correctly"""
    agent = IntelligentAgent()
    assert agent.status.value == "ready"
    assert len(agent.tools) == 3

@pytest.mark.asyncio
async def test_agent_processes_refund_request():
    """Test refund request processing"""
    agent = IntelligentAgent()
    message = Message(
        content="I need a refund for order #12345",
        timestamp=datetime.now(),
        user_id="test-user"
    )
    response = await agent.execute(message)
    assert response.success
    assert "refund" in response.content.lower()
```

## Documentation

### Updating Documentation

- Keep README.md up to date
- Add docstrings to all new functions and classes
- Update examples when adding new features
- Include inline comments for complex logic

### Documentation Style

Use Google-style docstrings:
```python
def process_message(message: str, max_length: int = 100) -> Dict[str, Any]:
    """Process a user message and return structured data.
    
    Args:
        message: The user's input message
        max_length: Maximum allowed message length
    
    Returns:
        A dictionary containing:
            - intent: Detected user intent
            - entities: Extracted entities
            - confidence: Confidence score
    
    Raises:
        ValueError: If message exceeds max_length
    """
```

## Project Structure

When adding new features, follow this structure:

```
hybrid-framework/
├── src/                    # Source code (if needed)
│   ├── agno/              # Agno-specific code
│   ├── agent_os/          # Agent OS integrations
│   └── bridge/            # Bridge implementations
├── examples/              # Example implementations
├── tests/                 # Test files
├── docs/                  # Documentation
└── scripts/               # Utility scripts
```

## Release Process

1. Update version in `setup.py` (if applicable)
2. Update CHANGELOG.md
3. Create a git tag: `git tag -a v1.0.0 -m "Release version 1.0.0"`
4. Push tags: `git push origin --tags`
5. Create GitHub release with release notes

## Getting Help

- **Discord**: Join our [community Discord](https://discord.gg/hybrid-framework)
- **GitHub Issues**: For bug reports and feature requests
- **Discussions**: For questions and general discussion
- **Email**: support@hybridframework.dev

## Recognition

Contributors will be recognized in:
- The CONTRIBUTORS.md file
- Release notes for significant contributions
- Our documentation site

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

Thank you for contributing to the Hybrid Framework! Your efforts help make AI development faster and more accessible for everyone.
