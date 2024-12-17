import logging
from argparse import ArgumentParser, Namespace
from pathlib import Path
from typing import Any, Dict

import yaml
from yaml.error import YAMLError

"""
Configure logging with a standardized format including timestamp, logger name,
log level, and message. The datetime format is set to ISO-like format for
better readability and parsing.

Format example:
2024-12-17 14:30:45 - HuggingFace-Dataset-Builder - INFO - Starting dataset upload
"""
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    level=logging.INFO,
)

"""
Create a logger instance specific to the HuggingFace Dataset Builder
This logger will be used throughout the application to maintain consistent
logging practices and make log filtering easier
"""
logger = logging.getLogger(name="HuggingFace-Dataset-Builder")


def parse_args() -> Namespace:
    """
    Parse command-line arguments for the dataset builder script.

    Creates an argument parser with options for configuring the dataset
    building process. Currently supports specifying the path to a
    configuration file.

    Returns:
        Namespace: An object containing the parsed command-line arguments.
            Attributes:
                config_path (Path): Path to the configuration YAML file.

    Example:
        ```python
        args = parse_args()
        config = read_yaml(args.config_path)
        ```
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

    Attempts to read and parse a YAML file from the specified path, with
    comprehensive error handling for common failure scenarios.

    Args:
        yaml_path (Path): Path to the YAML file to be read.

    Returns:
        Dict[str, Any]: The parsed YAML content as a dictionary.

    Raises:
        FileNotFoundError: If the specified YAML file does not exist.
        YAMLError: If the YAML file cannot be parsed due to syntax errors.
        PermissionError: If the process lacks permission to read the file.
        Exception: For any other unexpected errors during file reading.

    Example:
        ```python
        try:
            config = read_yaml(Path("config.yaml"))
            dataset_name = config["dataset"]["name"]
        except FileNotFoundError:
            logger.error("Config file not found")
        except YAMLError:
            logger.error("Invalid YAML syntax in config file")
        ```
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
