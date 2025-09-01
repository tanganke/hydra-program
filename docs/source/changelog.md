# Changelog

All notable changes to Hydra-Program will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Sphinx-based documentation with comprehensive guides and API reference
- Getting started tutorial with practical examples
- Configuration guide with advanced patterns
- Examples covering common use cases
- Contributing guidelines for developers

### Changed
- Enhanced documentation structure and navigation

## [0.1.1] - 2025-09-01

### Added
- Initial release of Hydra-Program framework
- `hprun` command for running configured programs
- `hpinit` command for initializing project templates
- Configuration template system
- Core serialization functionality
- Rich logging integration
- Support for Hydra configuration composition

### Features
- Command-line interface with two main commands:
  - `hprun`: Execute programs with Hydra configuration
  - `hpinit`: Initialize configuration templates
- Configuration management with Hydra integration
- Automatic configuration serialization/deserialization
- Template-based project initialization
- Support for configuration overrides via command line
- Rich console output for better user experience

### Dependencies
- hydra-core: Core Hydra functionality
- rich: Enhanced terminal output
- bidict: Bidirectional mapping support

## [0.1.0] - Initial Development

### Added
- Basic project structure
- Core CLI functionality
- Configuration template system
- Initial documentation
