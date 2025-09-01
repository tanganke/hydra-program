#!/usr/bin/env python3
"""
This is the CLI script that is executed when the user runs the `hprun` command.
The script is responsible for parsing the command-line arguments, loading the configuration file, and running the hydra program.
"""
import logging
import os

import hydra
from hydra.utils import instantiate
from omegaconf import DictConfig, OmegaConf

log = logging.getLogger(__name__)


def _get_default_config_path():
    for config_dir in ["config", "configs"]:
        for config_path_root in [os.getcwd()]:
            config_path = os.path.join(config_path_root, config_dir)
            if os.path.exists(config_path) and os.path.isdir(config_path):
                return os.path.abspath(config_path)
    return None


@hydra.main(
    config_path=_get_default_config_path(),
    config_name="hprun",
    version_base=None,
)
def main(cfg: DictConfig) -> None:
    """
    Main entry point for the HydraProgram command-line interface.

    This function serves as the primary entry point for the `hprun` CLI command.
    It is decorated with Hydra's main decorator to handle configuration management,
    command-line argument parsing, and configuration file loading.

    The function performs the following operations:
    1. Resolves any interpolations in the configuration using OmegaConf
    2. Instantiates the appropriate program class based on the configuration
    3. Executes the program's run method to perform the task

    Args:
        cfg (DictConfig): The Hydra configuration object containing all settings
            for the program task. This includes program configuration and other
            runtime parameters. The configuration is automatically loaded by Hydra
            from the specified config files and command-line overrides.

    Returns:
        None: This function doesn't return a value but executes the hydra
            program which may save results, log outputs, or perform other
            side effects as configured.
    """
    OmegaConf.resolve(cfg)
    program = instantiate(cfg)
    program.run()


if __name__ == "__main__":
    main()
