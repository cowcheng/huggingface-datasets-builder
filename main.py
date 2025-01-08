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
    Load and prepare DataFrame from CSV according to configuration.

    Args:
        config (Config): Configuration object containing dataset settings

    Returns:
        pd.DataFrame: Loaded and reordered DataFrame according to config

    Raises:
        FileNotFoundError: If annotation CSV file cannot be found
        KeyError: If specified columns are missing from the CSV
    """
    try:
        dataframe = pd.read_csv(
            filepath_or_buffer=config.dataset.annotation_path,
            sep="\t",
            low_memory=False,
        )
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
    Cast dataset columns to their specified feature types.

    Args:
        dataset (Dataset): Hugging Face dataset to modify
        cast_columns (Dict[str, str]): Mapping of column names to target feature types

    Returns:
        Dataset: Modified dataset with cast columns

    Raises:
        KeyError: If specified feature type is not supported
        Exception: For other casting failures
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
    Upload dataset to Hugging Face Hub with specified configuration.

    Args:
        datasets_dict (DatasetDict): Dataset dictionary to upload
        config (Config): Configuration containing Hugging Face settings

    Raises:
        Exception: If upload fails for any reason
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
    Create and upload a dataset to Hugging Face Hub from configuration.

    Main workflow function that:
    1. Loads and validates configuration
    2. Prepares dataset from CSV
    3. Casts columns to appropriate types
    4. Uploads to Hugging Face Hub

    Args:
        config_path (Path): Path to YAML configuration file

    Raises:
        Exception: For any failure in the dataset creation pipeline
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
    """
    Hugging Face Dataset Builder script.

    Creates and uploads datasets to Hugging Face Hub based on YAML configuration.
    Handles data loading, column casting, and dataset uploading with error logging.

    Usage:
        python script.py -c config.yaml
    """
    try:
        args = parse_args()
        create(config_path=args.config_path)
    except KeyboardInterrupt:
        logger.info(msg="Process interrupted by user")
        raise
    except Exception as e:
        logger.error(msg=f"Process failed: {e}")
        raise
