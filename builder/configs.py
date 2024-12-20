from typing import Dict, List

from pydantic import BaseModel, Field, model_validator
from typing_extensions import Self


class DatasetConfig(BaseModel):
    """
    Configuration for dataset processing and validation.

    This class defines the structure and requirements for processing a dataset,
    including file paths, column ordering, and data type casting specifications.

    Attributes:
        annotation_path (str): Path to the CSV file containing dataset annotations.
        dataframe_order (List[str]): Ordered list of column names defining the expected
            structure of the dataframe. This order will be maintained during processing.
        cast_columns (Dict[str, str]): Mapping of column names to their desired data types.
            For example: {"column_name": "int64", "another_column": "string"}.
        split (str): Dataset split identifier (e.g., "train", "validation", "test").

    Example:
        ```python
        config = DatasetConfig(
            annotation_path="path/to/annotations.csv",
            dataframe_order=["id", "text", "label"],
            cast_columns={"id": "int64", "text": "string", "label": "int32"},
            split="train"
        )
        ```

    Raises:
        ValueError: If any column specified in dataframe_order is missing from cast_columns.
    """

    annotation_path: str = Field(description="Path to annotation CSV file")
    dataframe_order: List[str] = Field(description="Order of columns in the dataframe")
    cast_columns: Dict[str, str] = Field(description="Column casting configuration")
    split: str = Field(description="Dataset split name")

    @model_validator(mode="after")
    def validate_columns_consistency(
        self,
    ) -> "DatasetConfig":
        """
        Validates that all columns in dataframe_order have specified cast types.

        Returns:
            DatasetConfig: The validated configuration object.

        Raises:
            ValueError: If any column in dataframe_order is missing from cast_columns.
        """
        missing_columns = set(self.dataframe_order) - set(self.cast_columns)

        if missing_columns:
            raise ValueError(
                "Missing cast types for columns: "
                f"{', '.join(sorted(missing_columns))}. "
                "Please add these columns to cast_columns with appropriate types."
            )
        return self


class HuggingFaceConfig(BaseModel):
    """
    Configuration for Hugging Face repository interaction.

    This class defines the parameters needed to interact with a Hugging Face repository,
    including repository identification, configuration, and access settings.

    Attributes:
        repo_id (str): The Hugging Face repository identifier in the format "username/repo-name"
            or "organization/repo-name".
        config_name (str): Name of the configuration to be used within the repository.
        commit_message (str): Message to be used when committing changes to the repository.
        private (bool): Whether the repository should be private (True) or public (False).
        revision (str): The specific revision or branch name to target in the repository.

    Example:
        ```python
        config = HuggingFaceConfig(
            repo_id="username/dataset-name",
            config_name="default",
            commit_message="Update dataset configuration",
            private=True,
            revision="main"
        )
        ```
    """

    repo_id: str = Field(description="Hugging Face repository ID")
    config_name: str = Field(description="Configuration name")
    commit_message: str = Field(description="Commit message")
    private: bool = Field(description="Repository privacy status")
    revision: str = Field(description="Repository revision/branch")


class Config(BaseModel):
    """
    Main configuration class combining dataset and Hugging Face settings.

    This class serves as the top-level configuration container, combining both
    dataset-specific settings and Hugging Face repository configurations into a
    single, validated configuration object.

    Attributes:
        dataset (DatasetConfig): Configuration for dataset processing and validation.
        huggingface (HuggingFaceConfig): Configuration for Hugging Face repository interaction.

    Example:
        ```python
        config = Config(
            dataset=DatasetConfig(
                annotation_path="path/to/annotations.csv",
                dataframe_order=["id", "text", "label"],
                cast_columns={"id": "int64", "text": "string", "label": "int32"},
                split="train"
            ),
            huggingface=HuggingFaceConfig(
                repo_id="username/dataset-name",
                config_name="default",
                commit_message="Update dataset",
                private=True,
                revision="main"
            )
        )
        ```
    """

    dataset: DatasetConfig = Field(description="Dataset configuration")
    huggingface: HuggingFaceConfig = Field(description="Hugging Face configuration")
