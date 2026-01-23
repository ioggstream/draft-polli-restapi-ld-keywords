#!/usr/bin/env python3
"""Convert YAML files in vocab/ to JSON files."""

import json
import sys
from pathlib import Path

import yaml


def convert_yaml_to_json(yaml_path: Path) -> int:
    """Convert a YAML file to JSON format.

    Args:
        yaml_path: Path to the YAML file

    Returns:
        0 if successful, 1 if there was an error
    """
    try:
        # Read YAML file
        with open(yaml_path, "r") as f:
            data = yaml.safe_load(f)

        # Determine output JSON path (same name, different extension)
        json_path = yaml_path.with_suffix(".json")

        # Write JSON file with proper formatting
        with open(json_path, "w") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
            f.write("\n")  # Add trailing newline

        print(f"✓ Generated {json_path} from {yaml_path}")
        return 0

    except Exception as e:
        print(f"✗ Error converting {yaml_path}: {e}", file=sys.stderr)
        return 1


def main():
    """Process all YAML files passed as arguments."""
    if len(sys.argv) < 2:
        print("Usage: yaml-to-json.py <yaml_file> [<yaml_file> ...]", file=sys.stderr)
        return 1

    exit_code = 0
    for yaml_file in sys.argv[1:]:
        yaml_path = Path(yaml_file)

        # Only process YAML files in vocab/ directory
        if yaml_path.parent.name == "vocab" and yaml_path.suffix in [".yaml", ".yml"]:
            result = convert_yaml_to_json(yaml_path)
            if result != 0:
                exit_code = result

    return exit_code


if __name__ == "__main__":
    sys.exit(main())
