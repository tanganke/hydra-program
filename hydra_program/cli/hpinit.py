#!/usr/bin/env python3
"""
This is the CLI script that is executed when the user runs the `hpinit` command.
The script is responsible for copying configuration templates from the package's
config_templates directory to a local 'config' directory in the current working directory.
"""
import argparse
import os
import shutil
import sys
from pathlib import Path


def get_config_templates_path():
    """Get the path to the config_templates directory in the package."""
    import importlib.resources

    # Use importlib.resources to get the path to the config_templates directory
    try:
        config_templates_path = Path(
            importlib.resources.files("hydra_program") / "config_templates"
        )
    except Exception as e:
        raise FileNotFoundError(
            "Could not locate config_templates using importlib.resources"
        ) from e

    if not config_templates_path.exists():
        raise FileNotFoundError(
            f"Config templates directory not found: {config_templates_path}"
        )

    return config_templates_path


def copy_config_templates(force=False):
    """
    Copy configuration templates to a 'config' directory in the current working directory.

    Args:
        force (bool): If True, overwrite existing files. If False, skip existing files.
    """
    # Get source and destination paths
    source_path = get_config_templates_path()
    dest_path = Path.cwd() / "config"

    print(f"Copying configuration templates from {source_path} to {dest_path}")

    # Create destination directory if it doesn't exist
    dest_path.mkdir(exist_ok=True)

    copied_files = []
    skipped_files = []

    def copy_recursive(src_dir, dst_dir):
        """Recursively copy files and directories."""
        for item in src_dir.iterdir():
            src_item = src_dir / item.name
            dst_item = dst_dir / item.name

            if src_item.is_file():
                # Check if file already exists
                if dst_item.exists() and not force:
                    skipped_files.append(str(dst_item.relative_to(dest_path)))
                    print(
                        f"  Skipping existing file: {dst_item.relative_to(dest_path)}"
                    )
                else:
                    # Create parent directory if it doesn't exist
                    dst_item.parent.mkdir(parents=True, exist_ok=True)
                    # Copy the file
                    shutil.copy2(src_item, dst_item)
                    copied_files.append(str(dst_item.relative_to(dest_path)))
                    status = "Overwriting" if dst_item.exists() and force else "Copying"
                    print(f"  {status}: {dst_item.relative_to(dest_path)}")

            elif src_item.is_dir():
                # Create directory and recursively copy contents
                dst_item.mkdir(exist_ok=True)
                copy_recursive(src_item, dst_item)

    try:
        copy_recursive(source_path, dest_path)

        # Print summary
        print(f"\nSummary:")
        print(f"  Copied {len(copied_files)} file(s)")
        if skipped_files:
            print(f"  Skipped {len(skipped_files)} existing file(s)")
            print(f"  Use --force to overwrite existing files")

        if copied_files or skipped_files:
            print(f"\nConfiguration templates have been initialized in: {dest_path}")
        else:
            print("No files to copy.")

    except Exception as e:
        print(f"Error copying configuration templates: {e}", file=sys.stderr)
        sys.exit(1)


def main():
    """Main entry point for the hpinit command."""
    parser = argparse.ArgumentParser(
        description="Initialize configuration templates for hydra-program",
        prog="hpinit",
    )
    parser.add_argument(
        "--force", action="store_true", help="Overwrite existing configuration files"
    )
    args = parser.parse_args()

    try:
        copy_config_templates(force=args.force)
    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nOperation cancelled by user.", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
