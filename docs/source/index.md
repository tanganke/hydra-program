# Hydra-Program Documentation

Welcome to Hydra-Program, a powerful framework for building configurable and reproducible programs using Facebook's Hydra configuration system.

## Overview

Hydra-Program is a framework that simplifies building command-line applications with sophisticated configuration management. It leverages Hydra's powerful configuration composition and override capabilities to create flexible, maintainable programs.

## Key Features

- **Configuration Management**: Easy-to-use configuration system based on Hydra
- **Template System**: Built-in configuration templates for quick project setup
- **Extensible Architecture**: Plugin-based system for custom functionality
- **CLI Tools**: Command-line utilities for initialization and execution
- **Serialization Support**: Automatic configuration serialization and deserialization

## Quick Start

Install Hydra-Program:

```bash
pip install hydra-program
```

Initialize a new project:

```bash
hpinit
```

Run your program:

```bash
hprun program=my_program
```

## Documentation Contents

```{toctree}
:maxdepth: 2
:caption: User Guide

installation
getting_started
configuration
examples
```

```{toctree}
:maxdepth: 2
:caption: API Reference

api/modules
```

```{toctree}
:maxdepth: 1
:caption: Development

contributing
changelog
```

## Indices and Tables

- {ref}`genindex`
- {ref}`modindex`
- {ref}`search`

