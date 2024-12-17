from pathlib import Path
from typing import Dict

import pandas as pd
from datasets import Dataset, DatasetDict

from builder.configs import Config
from builder.constants import DATA_TYPE_MAP
from builder.utils import logger, parse_args, read_yaml


def prepare_dataframe(
    config: Config,
) -> pd.DataFrame:
    """
    Load and prepare a pandas DataFrame from a CSV file according to configuration.

    Reads the CSV file specified in the configuration and reorders columns according
    to the defined order in the configuration.

    Args:
        config (Config): Configuration object containing dataset settings including
            the path to the CSV file and the desired column order.

    Returns:
        pd.DataFrame: Prepared DataFrame with columns ordered according to configuration.

    Raises:
        FileNotFoundError: If the specified CSV file does not exist.
        KeyError: If any column specified in the configuration is missing from the CSV.

    Example:
        ```python
        config = Config(
            dataset=DatasetConfig(
                annotation_path="path/to/data.csv",
                dataframe_order=["id", "text", "label"]
            )
        )
        df = prepare_dataframe(config)
        ```
    """
    try:
        dataframe = pd.read_csv(filepath_or_buffer=config.dataset.annotation_path)
        dataframe = dataframe[config.dataset.dataframe_order]
        logger.info(msg=f"Loaded dataframe with shape: {dataframe.shape}")
        return dataframe
    except FileNotFoundError:
        logger.error(msg=f"CSV file not found: {config.dataset.annotation_path}")
        raise
    except KeyError as e:
        logger.error(msg=f"Missing column in CSV: {e}")
        raise


def cast_dataset_columns(
    dataset: Dataset,
    cast_columns: Dict[str, str],
) -> Dataset:
    """
    Cast dataset columns to specified feature types.

    Processes each column in the dataset according to the casting configuration,
    converting them to the appropriate feature types (e.g., audio, image, video).
    String columns are skipped as they don't need casting.

    Args:
        dataset (Dataset): The Hugging Face dataset to process.
        cast_columns (Dict[str, str]): Mapping of column names to their target
            feature types. Valid types are defined in DATA_TYPE_MAP.

    Returns:
        Dataset: The processed dataset with columns cast to their specified types.

    Raises:
        KeyError: If an unknown feature type is specified in cast_columns.
        Exception: If column casting fails for any other reason.

    Example:
        ```python
        cast_config = {
            "image_path": "image",
            "audio_path": "audio",
            "text": "str"
        }
        dataset = cast_dataset_columns(dataset, cast_config)
        ```
    """
    for column, feature_type in cast_columns.items():
        if feature_type == "str":
            continue
        try:
            feature = DATA_TYPE_MAP[feature_type]
            dataset = dataset.cast_column(
                column=column,
                feature=feature,
            )
        except KeyError:
            logger.error(
                msg=f"Unknown feature type: {feature_type} for column: {column}"
            )
            raise
        except Exception as e:
            logger.error(msg=f"Error casting column {column}: {e}")
            raise
    return dataset


def push_to_huggingface(
    datasets_dict: DatasetDict,
    config: Config,
) -> None:
    """
    Upload a dataset to the Hugging Face Hub.

    Pushes the processed dataset to the Hugging Face Hub with specified
    configuration settings. The dataset is automatically sharded into 1GB chunks
    and external files (like images or audio) are embedded.

    Args:
        datasets_dict (DatasetDict): The dataset dictionary to upload, typically
            containing splits like 'train', 'validation', etc.
        config (Config): Configuration object containing Hugging Face-specific
            settings like repository ID and privacy status.

    Raises:
        Exception: If the upload process fails for any reason.

    Example:
        ```python
        datasets_dict = DatasetDict({
            "train": train_dataset,
            "validation": val_dataset
        })
        push_to_huggingface(datasets_dict, config)
        ```
    """
    try:
        datasets_dict.push_to_hub(
            repo_id=config.huggingface.repo_id,
            config_name=config.huggingface.config_name,
            commit_message=config.huggingface.commit_message,
            private=config.huggingface.private,
            revision=config.huggingface.revision,
            max_shard_size="1GB",
            embed_external_files=True,
        )
        logger.info(msg=f"Successfully pushed dataset to {config.huggingface.repo_id}")
    except Exception as e:
        logger.error(msg=f"Failed to push to Hugging Face Hub: {e}")
        raise


def create(
    config_path: Path,
) -> None:
    """
    Create and upload a dataset to Hugging Face Hub from a configuration file.

    This is the main orchestration function that handles the entire dataset
    creation and upload process. It performs the following steps:
    1. Loads and validates the configuration
    2. Prepares the dataset from the source CSV
    3. Casts columns to their specified types
    4. Uploads the processed dataset to Hugging Face Hub

    Args:
        config_path (Path): Path to the YAML configuration file containing all
            necessary settings for dataset creation and upload.

    Raises:
        Exception: If any step in the dataset creation process fails.
            The specific exception type depends on the failing step.

    Example:
        ```python
        try:
            create(Path("config.yaml"))
        except Exception as e:
            print(f"Dataset creation failed: {e}")
        ```
    """
    try:
        # Load and validate configuration
        config_dict = read_yaml(yaml_path=config_path)
        config = Config(**config_dict)
        logger.info(msg=f"Loaded configuration: {config}")

        # Prepare dataset
        dataframe = prepare_dataframe(config=config)
        dataset = Dataset.from_pandas(df=dataframe)

        # Cast columns
        dataset = cast_dataset_columns(
            dataset=dataset,
            cast_columns=config.dataset.cast_columns,
        )

        # Push to HuggingFace
        datasets_dict = DatasetDict({config.dataset.split: dataset})
        push_to_huggingface(
            datasets_dict=datasets_dict,
            config=config,
        )

    except Exception as e:
        logger.error(msg=f"Dataset creation failed: {e}")
        raise


if __name__ == "__main__":
    try:
        args = parse_args()
        create(config_path=args.config_path)
    except KeyboardInterrupt:
        logger.info(msg="Process interrupted by user")
        raise
    except Exception as e:
        logger.error(msg=f"Process failed: {e}")
        raise
