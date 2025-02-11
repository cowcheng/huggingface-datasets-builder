import logging
from argparse import ArgumentParser, Namespace
from pathlib import Path
from typing import Any, Dict

import yaml

# Configure logging to display timestamp, logger name, log level, and message
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    level=logging.INFO,
)

# Create a logger instance for this script
logger = logging.getLogger(name="HuggingFace-Dataset-Builder")


def parse_args() -> Namespace:
    """
    Parses command-line arguments for the dataset creation script.

    Returns:
        Namespace: An object containing the parsed command-line arguments.
    """
    parser = ArgumentParser(description="Create and upload a dataset to Hugging Face.")
    parser.add_argument(
        "-c",
        "--configs_path",
        type=Path,
        required=True,
        help="Path to the configurations file",
    )
    return parser.parse_args()


def read_yaml(
    yaml_path: Path,
) -> Dict[str, Any]:
    """
    Reads a YAML configuration file and returns its contents as a dictionary.

    Args:
        yaml_path (Path): The path to the YAML configuration file.

    Returns:
        Dict[str, Any]: A dictionary containing the parsed YAML data.
    """
    with open(yaml_path) as fs:
        configs = yaml.safe_load(stream=fs)
    return configs
