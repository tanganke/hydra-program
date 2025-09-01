# Hydra-Program Documentation

This directory contains the Sphinx-based documentation for Hydra-Program.

## Building Documentation

### Prerequisites

Install the documentation dependencies:

```bash
pip install sphinx sphinx_rtd_theme sphinx-autodoc-typehints myst-parser
```

### Building HTML Documentation

```bash
# From the docs directory
make html

# Or using sphinx-build directly
sphinx-build -b html source build/html
```

The built documentation will be available in `build/html/index.html`.

### Live Reload Development

For development, you can use live reload to automatically rebuild docs when files change:

```bash
# Install sphinx-autobuild
pip install sphinx-autobuild

# Start live reload server
make livehtml
```

This will start a server at `http://localhost:8000` that automatically rebuilds and refreshes when you save changes.

### Other Build Targets

```bash
# Clean build directory
make clean

# Check external links
make linkcheck

# Build PDF (requires LaTeX)
make latexpdf

# See all available targets
make help
```

## Documentation Structure

- `source/index.md` - Main documentation page
- `source/installation.md` - Installation guide
- `source/getting_started.md` - Getting started tutorial
- `source/configuration.md` - Configuration guide
- `source/examples.md` - Practical examples
- `source/api/` - API reference documentation
- `source/contributing.md` - Contributing guidelines
- `source/changelog.md` - Project changelog
- `source/conf.py` - Sphinx configuration
- `source/_static/` - Static files (CSS, images, etc.)

## Writing Documentation

### Format

The documentation is written in Markdown using MyST parser, which allows you to use Sphinx directives in Markdown files.

### API Documentation

API documentation is automatically generated from docstrings using Sphinx's autodoc extension. Make sure your code has proper docstrings following Google or NumPy style.

### Cross-references

You can create cross-references using MyST syntax:

```markdown
{doc}`getting_started`  # Link to another document
{ref}`section-label`    # Link to a section
{func}`module.function` # Link to a function
```

### Code Blocks

Use standard Markdown code blocks with syntax highlighting:

````markdown
```python
def example_function():
    return "Hello, World!"
```
````

### Admonitions

Use Sphinx admonitions for notes, warnings, etc:

```markdown
```{note}
This is a note admonition.
```

```{warning}
This is a warning admonition.
```
```

## Contributing to Documentation

1. Follow the existing structure and style
2. Use clear, concise language
3. Include practical examples
4. Test your documentation builds without errors
5. Update the table of contents if adding new pages

## Deployment

The documentation can be deployed to various platforms:

- **GitHub Pages**: Use GitHub Actions to build and deploy
- **Read the Docs**: Connect your repository for automatic builds
- **Netlify**: For more advanced hosting needs

Example GitHub Actions workflow for deployment is available in the project's `.github/workflows/` directory.
