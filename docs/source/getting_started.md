# Getting Started

This guide will walk you through creating your first Hydra-Program application.

## Step 1: Initialize a New Project

Create a new directory for your project and initialize it with Hydra-Program:

```bash
mkdir my-hydra-project
cd my-hydra-project
hpinit
```

This command creates a `config` directory with template configuration files:

```
config/
├── hprun.yaml          # Main configuration file
├── hydra/
│   └── default.yaml    # Hydra framework settings
└── path/
    └── default.yaml    # Path configurations
```

## Step 2: Create Your First Program

Create a simple program class. Save this as `my_program.py`:

```python
from omegaconf import DictConfig

class MyProgram:
    """A simple example program."""
    
    def __init__(self, message: str = "Hello, World!", count: int = 1):
        self.message = message
        self.count = count
    
    def run(self):
        """Run the program."""
        for i in range(self.count):
            print(f"{i + 1}: {self.message}")

# For Hydra instantiation
def create_program(message: str = "Hello, World!", count: int = 1):
    return MyProgram(message, count)
```

## Step 3: Configure Your Program

Create a configuration file for your program at `config/program/my_program.yaml`:

```yaml
# @package _global_
defaults:
  - base_config

_target_: my_program.create_program
message: "Hello from Hydra-Program!"
count: 3
```

Update your main configuration file `config/hprun.yaml`:

```yaml
defaults:
  - hydra: default
  - path: default
  - program: my_program

# You can override any configuration here
```

## Step 4: Run Your Program

Execute your program using the `hprun` command:

```bash
hprun
```

You should see output like:

```
1: Hello from Hydra-Program!
2: Hello from Hydra-Program!
3: Hello from Hydra-Program!
```

## Step 5: Configuration Overrides

One of Hydra's powerful features is the ability to override configuration from the command line:

```bash
# Change the message
hprun message="Custom message!"

# Change the count
hprun count=5

# Change multiple parameters
hprun message="Testing" count=2
```

## Step 6: Using Different Configurations

You can create multiple program configurations and switch between them:

Create `config/program/greeting.yaml`:

```yaml
# @package _global_
defaults:
  - base_config

_target_: my_program.create_program
message: "Greetings from Hydra!"
count: 1
```

Run with the different configuration:

```bash
hprun program=greeting
```

## Advanced Features

### Working with Complex Configurations

Hydra-Program supports complex nested configurations. Here's an example with a more sophisticated program:

```python
# advanced_program.py
from dataclasses import dataclass
from typing import List, Optional
from omegaconf import DictConfig

@dataclass
class DatabaseConfig:
    host: str = "localhost"
    port: int = 5432
    database: str = "mydb"

@dataclass
class ProcessingConfig:
    batch_size: int = 100
    max_workers: int = 4
    timeout: float = 30.0

class AdvancedProgram:
    def __init__(self, db: DatabaseConfig, processing: ProcessingConfig, debug: bool = False):
        self.db = db
        self.processing = processing
        self.debug = debug
    
    def run(self):
        print(f"Connecting to {self.db.host}:{self.db.port}/{self.db.database}")
        print(f"Processing with {self.processing.max_workers} workers")
        print(f"Batch size: {self.processing.batch_size}")
        if self.debug:
            print("Debug mode enabled")

def create_advanced_program(db: DictConfig, processing: DictConfig, debug: bool = False):
    return AdvancedProgram(
        db=DatabaseConfig(**db),
        processing=ProcessingConfig(**processing),
        debug=debug
    )
```

Configuration file `config/program/advanced.yaml`:

```yaml
# @package _global_
defaults:
  - base_config

_target_: advanced_program.create_advanced_program

db:
  host: "localhost"
  port: 5432
  database: "production"

processing:
  batch_size: 200
  max_workers: 8
  timeout: 60.0

debug: false
```

Run with overrides:

```bash
hprun program=advanced db.host=remote-server processing.batch_size=50 debug=true
```

## Next Steps

- Learn more about [Configuration](configuration.md) management
- Explore [Examples](examples.md) for common patterns
- Check the [API Reference](api/modules.md) for detailed documentation

## Tips

1. **Use composition**: Break down complex configurations into smaller, reusable pieces
2. **Leverage defaults**: Use Hydra's defaults list to compose configurations
3. **Command-line overrides**: Take advantage of Hydra's powerful override syntax
4. **Environment-specific configs**: Create different configurations for development, testing, and production
5. **Validation**: Consider using dataclasses or Pydantic models for configuration validation
