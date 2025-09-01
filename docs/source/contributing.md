# Contributing to Hydra-Program

We welcome contributions to Hydra-Program! This document provides guidelines for contributing to the project.

## Development Setup

### Prerequisites

- Python 3.9 or later
- Git

### Setting up the Development Environment

1. Fork the repository on GitHub
2. Clone your fork locally:

```bash
git clone https://github.com/your-username/hydra-program.git
cd hydra-program
```

3. Create a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

4. Install the package in development mode:

```bash
pip install -e ".[dev]"
```

## Development Workflow

### Making Changes

1. Create a new branch for your feature or fix:

```bash
git checkout -b feature/your-feature-name
```

2. Make your changes
3. Write or update tests as needed
4. Update documentation if necessary
5. Ensure your code follows the project's coding standards

### Testing

Run the test suite to ensure your changes don't break existing functionality:

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=hydra_program

# Run specific test file
pytest tests/test_specific.py
```

### Code Quality

We use several tools to maintain code quality:

```bash
# Format code with black
black hydra_program tests

# Sort imports with isort
isort hydra_program tests

# Check code with flake8
flake8 hydra_program tests

# Type checking with mypy
mypy hydra_program
```

### Documentation

If you're adding new features or changing existing functionality:

1. Update docstrings in the code
2. Add or update relevant documentation files
3. Build the documentation locally to test:

```bash
cd docs
make html
```

## Submitting Changes

### Pull Request Process

1. Push your changes to your fork:

```bash
git push origin feature/your-feature-name
```

2. Create a pull request on GitHub
3. Provide a clear description of your changes
4. Link any relevant issues
5. Ensure all checks pass

### Pull Request Guidelines

- **Clear title**: Use a descriptive title that summarizes the change
- **Detailed description**: Explain what you changed and why
- **Test coverage**: Include tests for new functionality
- **Documentation**: Update docs for user-facing changes
- **Backwards compatibility**: Avoid breaking changes when possible
- **Small focused changes**: Keep PRs focused on a single concern

## Coding Standards

### Python Style

- Follow PEP 8 guidelines
- Use type hints where appropriate
- Write clear, descriptive docstrings
- Keep functions and classes focused and small

### Documentation Style

- Use Google-style docstrings
- Include examples in docstrings when helpful
- Write clear, concise documentation
- Update the changelog for notable changes

### Example Docstring

```python
def process_data(data: List[str], transform: bool = True) -> Dict[str, Any]:
    """Process a list of data items.
    
    This function takes a list of string data items and processes them
    according to the specified parameters.
    
    Args:
        data: List of string data items to process.
        transform: Whether to apply transformations to the data.
    
    Returns:
        A dictionary containing the processed results with keys:
        - 'count': Number of items processed
        - 'items': List of processed items
    
    Example:
        >>> data = ['item1', 'item2', 'item3']
        >>> result = process_data(data, transform=True)
        >>> print(result['count'])
        3
    """
```

## Types of Contributions

### Bug Reports

When reporting bugs, please include:

- Clear description of the issue
- Steps to reproduce
- Expected vs. actual behavior
- Environment details (OS, Python version, etc.)
- Minimal code example if applicable

### Feature Requests

For feature requests, please:

- Describe the use case
- Explain why the feature would be valuable
- Consider backwards compatibility
- Provide examples of how it would work

### Code Contributions

We welcome:

- Bug fixes
- New features
- Performance improvements
- Documentation improvements
- Test coverage improvements

## Project Structure

Understanding the project structure will help you contribute effectively:

```
hydra-program/
├── hydra_program/           # Main package
│   ├── __init__.py
│   ├── cli/                 # Command-line interface
│   │   ├── hprun.py        # Main runner command
│   │   └── hpinit.py       # Initialization command
│   ├── core/               # Core functionality
│   │   ├── serialization.py # Configuration serialization
│   │   └── utils.py        # Utility functions
│   └── config_templates/   # Default configuration templates
├── tests/                  # Test suite
├── docs/                   # Documentation
├── pyproject.toml         # Project configuration
└── README.md              # Project overview
```

## Release Process

Releases are managed by project maintainers. The process includes:

1. Version bump in `pyproject.toml`
2. Update `CHANGELOG.md`
3. Create a git tag
4. Build and publish to PyPI
5. Create GitHub release

## Getting Help

If you need help with contributing:

- Open an issue for discussion
- Check existing issues and pull requests
- Ask questions in discussions
- Contact the maintainers

## Recognition

Contributors are recognized in several ways:

- Listed in the project's contributors
- Mentioned in release notes for significant contributions
- Added to the `AUTHORS` file for ongoing contributors

Thank you for contributing to Hydra-Program!
