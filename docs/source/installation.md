# Installation

## Requirements

Hydra-Program requires Python 3.9 or later.

## From PyPI

The easiest way to install Hydra-Program is from PyPI:

```bash
pip install hydra-program
```

## From Source

To install from source, clone the repository and install in development mode:

```bash
git clone https://github.com/tanganke/hydra-program.git
cd hydra-program
pip install -e .
```

## Verify Installation

After installation, verify that the CLI commands are available:

```bash
# Check hprun command
hprun --help

# Check hpinit command
hpinit --help
```

You should see help messages for both commands if the installation was successful.

## Dependencies

Hydra-Program depends on:

- **hydra-core**: The core Hydra configuration system
- **rich**: For beautiful terminal output and logging
- **bidict**: For bidirectional mapping support in serialization

These dependencies will be automatically installed when you install Hydra-Program.

## Development Dependencies

For development, you may want to install additional dependencies:

```bash
pip install -e ".[dev]"
```

This includes tools for testing, linting, and documentation generation.
