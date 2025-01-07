import logging
from argparse import ArgumentParser, Namespace
from pathlib import Path
from typing import Any, Dict

import yaml
from yaml.error import YAMLError

"""
Configure basic logging settings for the application.

Sets up logging with timestamp, logger name, level and message format.
Default level is set to INFO for general execution logging.
"""
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    level=logging.INFO,
)

"""
Logger instance for the Hugging Face Dataset Builder application.
"""
logger = logging.getLogger(name="HuggingFace-Dataset-Builder")


def parse_args() -> Namespace:
    """
    Parse command line arguments for the dataset builder.

    Returns:
        Namespace: Parsed argument object containing:
            config_path (Path): Path to the YAML configuration file
    """
    parser = ArgumentParser(description="Create and upload a dataset to Hugging Face.")
    parser.add_argument(
        "-c",
        "--config_path",
        type=Path,
        required=True,
        help="Path to the configuration file",
    )
    return parser.parse_args()


def read_yaml(
    yaml_path: Path,
) -> Dict[str, Any]:
    """
    Read and parse a YAML configuration file.

    Args:
        yaml_path (Path): Path to the YAML file to read

    Returns:
        Dict[str, Any]: Parsed YAML content as a dictionary

    Raises:
        FileNotFoundError: If the specified file doesn't exist
        YAMLError: If the YAML file is malformed
        PermissionError: If there are insufficient permissions to read the file
        Exception: For other unexpected errors during file reading/parsing
    """
    try:
        yaml_path = Path(yaml_path)
        if not yaml_path.exists():
            raise FileNotFoundError(f"Config file not found: {yaml_path}")

        with yaml_path.open("r", encoding="utf-8") as file:
            return yaml.safe_load(stream=file)

    except YAMLError as e:
        logger.error(msg=f"Failed to parse YAML file: {e}")
        raise
    except PermissionError:
        logger.error(msg=f"Permission denied when reading: {yaml_path}")
        raise
    except Exception as e:
        logger.error(msg=f"Unexpected error reading YAML file: {e}")
        raise
