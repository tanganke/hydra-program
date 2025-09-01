# Hydra-Program

A hydra-based program running framework for building configurable and reproducible applications.

## Overview

Hydra-Program provides a powerful framework for creating command-line applications with sophisticated configuration management. Built on top of Facebook's Hydra, it offers:

- **Easy Configuration Management**: Hierarchical configuration with composition support
- **CLI Tools**: Ready-to-use command-line utilities (`hprun`, `hpinit`)
- **Template System**: Quick project initialization with sensible defaults
- **Flexible Architecture**: Support for complex program structures and workflows

## Quick Start

### Installation

```bash
pip install hydra-program
```

### Initialize a New Project

```bash
mkdir my-project && cd my-project
hpinit
```

This creates a `config/` directory with template configurations.

### Create Your Program

```python
# my_program.py
class MyProgram:
    def __init__(self, message: str = "Hello, World!", count: int = 1):
        self.message = message
        self.count = count
    
    def run(self):
        for i in range(self.count):
            print(f"{i + 1}: {self.message}")

def create_program(message: str = "Hello, World!", count: int = 1):
    return MyProgram(message, count)
```

### Configure Your Program

Create `config/program/my_program.yaml`:

```yaml
# @package _global_
_target_: my_program.create_program
message: "Hello from Hydra-Program!"
count: 3
```

Update `config/hprun.yaml`:

```yaml
defaults:
  - hydra: default
  - path: default
  - program: my_program
```

### Run Your Program

```bash
# Run with default configuration
hprun

# Override configuration
hprun message="Custom message!" count=5

# Use different program configuration
hprun program=other_program
```

## Documentation

Comprehensive documentation is available with:

- **[Getting Started Guide](docs/source/getting_started.md)**: Step-by-step tutorial
- **[Configuration Guide](docs/source/configuration.md)**: Advanced configuration patterns
- **[Examples](docs/source/examples.md)**: Real-world use cases
- **[API Reference](docs/source/api/modules.md)**: Complete API documentation

### Building Documentation

```bash
cd docs
pip install -r requirements.txt  # or pip install -e ".[docs]"
sphinx-build -b html source build/html
```

## Features

### Configuration Management

- **Composition**: Build complex configurations from simple components
- **Overrides**: Command-line parameter overrides
- **Environment Support**: Different configurations for dev/staging/production
- **Validation**: Type-safe configuration with structured configs
- **Interpolation**: Variable substitution and environment variables

### CLI Tools

- **`hprun`**: Execute configured programs with Hydra integration
- **`hpinit`**: Initialize project templates and configuration structure

### Advanced Features

- **Multirun Support**: Parameter sweeps and hyperparameter optimization
- **Plugin System**: Extensible architecture for custom functionality
- **Rich Logging**: Beautiful console output with progress indicators
- **Serialization**: Automatic configuration persistence

## Examples

### Data Processing Pipeline

```python
# data_processor.py
from dataclasses import dataclass
from typing import List, Optional

@dataclass
class ProcessingConfig:
    input_file: str
    output_file: str
    columns: Optional[List[str]] = None
    remove_duplicates: bool = True

class DataProcessor:
    def __init__(self, config: ProcessingConfig):
        self.config = config
    
    def run(self):
        # Your processing logic here
        pass
```

```yaml
# config/program/data_processing.yaml
_target_: data_processor.DataProcessor
config:
  input_file: "${path.data_dir}/input.csv"
  output_file: "${path.output_dir}/processed.csv"
  columns: ["name", "value", "timestamp"]
```

### Machine Learning Training

```bash
# Run with different models
hprun program=ml_training model=transformer
hprun program=ml_training model=lstm

# Hyperparameter sweep
hprun -m program=ml_training model.layers=6,8,12 optimizer.lr=0.001,0.01
```

## Contributing

We welcome contributions! Please see our [Contributing Guide](docs/source/contributing.md) for details.

### Development Setup

```bash
git clone https://github.com/tanganke/hydra-program.git
cd hydra-program
pip install -e ".[dev]"
```

### Running Tests

```bash
pytest
pytest --cov=hydra_program  # With coverage
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Links

- **Documentation**: [Available in docs/](docs/)
- **Repository**: [https://github.com/tanganke/hydra-program](https://github.com/tanganke/hydra-program)
- **Issues**: [https://github.com/tanganke/hydra-program/issues](https://github.com/tanganke/hydra-program/issues)
- **PyPI**: [https://pypi.org/project/hydra-program/](https://pypi.org/project/hydra-program/)
