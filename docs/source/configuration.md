# Configuration Guide

This guide covers the configuration system in Hydra-Program, which is built on top of Facebook's Hydra framework.

## Configuration Structure

Hydra-Program uses a hierarchical configuration system with the following structure:

```
config/
├── hprun.yaml              # Main entry point
├── hydra/                  # Hydra framework settings
│   ├── default.yaml
│   ├── help/
│   │   └── hprun.yaml
│   └── job_logging/
│       └── rich_logging.yaml
├── path/                   # Path configurations
│   └── default.yaml
└── program/                # Your program configurations
    ├── my_program.yaml
    └── another_program.yaml
```

## Main Configuration File

The `config/hprun.yaml` file is the main entry point:

```yaml
defaults:
  - hydra: default          # Hydra settings
  - path: default          # Path settings
  - program: my_program    # Which program to run

# Global overrides can go here
debug: false
verbose: true
```

## Program Configurations

Program configurations define how to instantiate and configure your program classes. They use Hydra's `_target_` mechanism for object instantiation.

### Basic Program Configuration

```yaml
# config/program/simple.yaml
# @package _global_
defaults:
  - base_config

_target_: my_module.MyProgram
parameter1: "value1"
parameter2: 42
parameter3: true
```

### Complex Program Configuration

```yaml
# config/program/complex.yaml
# @package _global_
defaults:
  - base_config

_target_: my_module.ComplexProgram

database:
  host: "localhost"
  port: 5432
  username: "user"
  password: "secret"

processing:
  batch_size: 1000
  num_workers: 4
  timeout: 300

features:
  enable_cache: true
  enable_logging: true
  log_level: "INFO"
```

## Configuration Composition

Hydra's defaults system allows you to compose configurations from multiple files:

```yaml
# config/program/production.yaml
defaults:
  - base_config
  - database: production
  - logging: structured
  - _self_

_target_: my_module.ProductionProgram
environment: "production"
```

This configuration composes:
- Base configuration settings
- Production database configuration
- Structured logging configuration
- Its own settings (via `_self_`)

## Configuration Groups

You can organize related configurations into groups:

### Database Configurations

```yaml
# config/database/development.yaml
host: "localhost"
port: 5432
database: "dev_db"
username: "dev_user"
password: "dev_pass"
```

```yaml
# config/database/production.yaml
host: "prod-server.company.com"
port: 5432
database: "prod_db"
username: "${oc.env:DB_USERNAME}"
password: "${oc.env:DB_PASSWORD}"
```

### Logging Configurations

```yaml
# config/logging/simple.yaml
level: "INFO"
format: "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
```

```yaml
# config/logging/structured.yaml
level: "DEBUG"
format: "json"
handlers:
  - console
  - file
```

## Environment Variables and Interpolation

Hydra supports variable interpolation and environment variable access:

```yaml
# Using environment variables
database:
  host: "${oc.env:DB_HOST,localhost}"  # Default to localhost if not set
  password: "${oc.env:DB_PASSWORD}"    # Required environment variable

# Using interpolation
paths:
  data_dir: "/data"
  input_file: "${paths.data_dir}/input.csv"
  output_file: "${paths.data_dir}/output.csv"
```

## Overrides

### Command-line Overrides

Override any configuration parameter from the command line:

```bash
# Simple overrides
hprun database.host=new-server database.port=3306

# List and dictionary overrides
hprun processing.batch_sizes=[100,200,300]
hprun features='{enable_cache: false, log_level: DEBUG}'

# Using different configuration groups
hprun database=production logging=structured
```

### Multi-run

Run your program with multiple configurations:

```bash
# Run with different batch sizes
hprun -m processing.batch_size=100,200,500

# Run with different databases and programs
hprun -m database=dev,prod program=training,inference
```

## Advanced Configuration Patterns

### Conditional Configuration

```yaml
# config/program/conditional.yaml
defaults:
  - base_config
  - database: development
  - logging: simple

# Override defaults based on environment
defaults:
  - override database: production
  - override logging: structured

_target_: my_module.MyProgram

# Use conditional values
debug: ${oc.env:DEBUG,false}
workers: ${oc.decode:${oc.env:WORKERS,4}}
```

### Nested Instantiation

```yaml
# config/program/nested.yaml
# @package _global_
defaults:
  - base_config

_target_: my_module.ComplexProgram

# Nested object instantiation
optimizer:
  _target_: torch.optim.Adam
  lr: 0.001
  weight_decay: 0.0001

model:
  _target_: my_module.MyModel
  hidden_size: 128
  num_layers: 3
```

### Configuration Inheritance

```yaml
# config/program/base_model.yaml
# @package _global_
_target_: my_module.BaseModel
input_size: 784
hidden_size: 128
output_size: 10
learning_rate: 0.001
```

```yaml
# config/program/improved_model.yaml
# @package _global_
defaults:
  - base_model

# Override specific parameters
hidden_size: 256
learning_rate: 0.0005

# Add new parameters
dropout_rate: 0.2
batch_norm: true
```

## Path Configuration

The path configuration system helps manage file paths across different environments:

```yaml
# config/path/default.yaml
data_dir: "${oc.env:DATA_DIR,./data}"
output_dir: "${oc.env:OUTPUT_DIR,./output}"
log_dir: "${oc.env:LOG_DIR,./logs}"

# Derived paths
train_data: "${data_dir}/train.csv"
test_data: "${data_dir}/test.csv"
model_path: "${output_dir}/model.pkl"
```

## Hydra Settings

Customize Hydra's behavior through hydra configurations:

```yaml
# config/hydra/custom.yaml
defaults:
  - _self_
  - job_logging: rich_logging

run:
  dir: ./outputs/${now:%Y-%m-%d}/${now:%H-%M-%S}

sweep:
  dir: ./multirun/${now:%Y-%m-%d}/${now:%H-%M-%S}
  subdir: ${hydra.job.num}

job:
  name: ${program}
  chdir: true
```

## Best Practices

1. **Use meaningful names**: Choose descriptive names for configuration files and parameters
2. **Group related configs**: Organize configurations into logical groups (database, logging, etc.)
3. **Document your configs**: Add comments to explain complex configurations
4. **Use environment variables**: For sensitive data and environment-specific settings
5. **Validate configurations**: Use dataclasses or Pydantic models for type checking
6. **Keep it DRY**: Use composition and inheritance to avoid duplication
7. **Test configurations**: Create tests to validate your configuration combinations

## Troubleshooting

### Common Issues

1. **Missing configuration files**: Ensure all referenced configurations exist
2. **Import errors**: Check that `_target_` paths are correct and modules are importable
3. **Type mismatches**: Verify that configuration values match expected types
4. **Circular dependencies**: Avoid circular references in configuration composition

### Debugging

Use Hydra's built-in debugging features:

```bash
# Print the final configuration
hprun --cfg job

# Print configuration sources
hprun --info

# Validate configuration without running
hprun --validate-config
```
