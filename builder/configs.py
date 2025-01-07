from typing import Dict, List

from pydantic import BaseModel, Field, model_validator


class DatasetConfig(BaseModel):
    """
    Configuration class for dataset processing and validation.

    This class handles dataset configuration including annotation file paths,
    column ordering, data type casting, and dataset split information.

    Attributes:
        annotation_path (str): Path to the CSV file containing annotations
        dataframe_order (List[str]): Ordered list specifying column arrangement
        cast_columns (Dict[str, str]): Mapping of column names to their target data types
        split (str): Dataset partition identifier (e.g., 'train', 'test', 'val')
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
        Validates that all columns specified in dataframe_order have casting types defined.

        Returns:
            DatasetConfig: Self reference if validation passes

        Raises:
            ValueError: If any column in dataframe_order lacks a casting type definition
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
    Configuration class for Hugging Face repository settings.

    This class manages configuration parameters for interacting with
    Hugging Face repositories, including repository identification,
    versioning, and access control.

    Attributes:
        repo_id (str): Identifier for the Hugging Face repository
        config_name (str): Name of the configuration to use
        commit_message (str): Message to use when committing changes
        private (bool): Whether the repository should be private
        revision (str): Branch or revision identifier
    """

    repo_id: str = Field(description="Hugging Face repository ID")
    config_name: str = Field(description="Configuration name")
    commit_message: str = Field(description="Commit message")
    private: bool = Field(description="Repository privacy status")
    revision: str = Field(description="Repository revision/branch")


class Config(BaseModel):
    """
    Root configuration class combining dataset and Hugging Face settings.

    This class serves as the top-level configuration container, combining
    both dataset processing settings and Hugging Face repository configuration.

    Attributes:
        dataset (DatasetConfig): Configuration for dataset processing
        huggingface (HuggingFaceConfig): Configuration for Hugging Face integration
    """

    dataset: DatasetConfig = Field(description="Dataset configuration")
    huggingface: HuggingFaceConfig = Field(description="Hugging Face configuration")
