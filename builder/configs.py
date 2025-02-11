from typing import Dict, List

from pydantic import BaseModel, Field, model_validator


class DatasetConfigs(BaseModel):
    """
    Configuration for dataset processing.

    Attributes:
        annotation_path (str): Path to the dataset annotation file.
        dataframe_order (List[str]): Order of columns expected in the dataframe.
        cast_columns (Dict[str, str]): Mapping of column names to their expected data types.
        split (str): Dataset split identifier (e.g., 'train', 'test', 'validation').
    """

    annotation_path: str = Field()
    dataframe_order: List[str] = Field()
    cast_columns: Dict[str, str] = Field()
    split: str = Field()

    @model_validator(mode="after")
    def validate_columns_consistency(
        self,
    ) -> "DatasetConfigs":
        """
        Validates that all columns in dataframe_order have corresponding cast types in cast_columns.

        Raises:
            ValueError: If any column in dataframe_order is missing from cast_columns.

        Returns:
            DatasetConfigs: The validated dataset configuration instance.
        """
        missing_columns = set(self.dataframe_order) - set(self.cast_columns)
        if missing_columns:
            raise ValueError(
                "Missing cast types for columns: "
                f"{', '.join(sorted(missing_columns))}. "
                "Please add these columns to cast_columns with appropriate types."
            )
        return self


class HuggingFaceConfigs(BaseModel):
    """
    Configuration for Hugging Face dataset repository settings.

    Attributes:
        repo_id (str): Identifier for the Hugging Face dataset repository.
        config_name (str): Configuration name for the dataset.
        commit_message (str): Commit message to use when updating the repository.
        private (bool): Whether the repository is private.
    """

    repo_id: str = Field()
    config_name: str = Field()
    commit_message: str = Field()
    private: bool = Field()


class Configs(BaseModel):
    """
    Root configuration model that holds dataset and Hugging Face settings.

    Attributes:
        dataset (DatasetConfigs): Dataset processing configurations.
        huggingface (HuggingFaceConfigs): Hugging Face repository configurations.
    """

    dataset: DatasetConfigs = Field()
    huggingface: HuggingFaceConfigs = Field()
