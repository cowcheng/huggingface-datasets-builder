import pandas as pd
from datasets import Dataset, DatasetDict

from builder.configs import Configs
from builder.constants import DATA_TYPE_MAP
from builder.utils import logger, parse_args, read_yaml


def create(
    configs: Configs,
) -> None:
    """
    Creates a Hugging Face dataset from a CSV annotation file and uploads it to the Hugging Face Hub.

    Args:
        configs (Configs): A configuration object containing dataset parameters,
                           Hugging Face repository details, and column specifications.
    """
    logger.info(msg=f"Configs: {configs}")

    dataframe = pd.read_csv(
        filepath_or_buffer=configs.dataset.annotation_path,
        sep="\t",
        low_memory=False,
    )
    dataframe = dataframe[configs.dataset.dataframe_order]
    dataset = Dataset.from_pandas(df=dataframe)
    for column, feature_type in configs.dataset.cast_columns.items():
        if feature_type == "str":
            continue
        feature = DATA_TYPE_MAP[feature_type]
        dataset = dataset.cast_column(
            column=column,
            feature=feature,
        )
    logger.info(msg=f"Dataset: {dataset}")

    datasets_dict = DatasetDict({configs.dataset.split: dataset})
    datasets_dict.push_to_hub(
        repo_id=configs.huggingface.repo_id,
        config_name=configs.huggingface.config_name,
        commit_message=configs.huggingface.commit_message,
        private=configs.huggingface.private,
        max_shard_size="1GB",
        embed_external_files=True,
    )
    logger.info(msg="Dataset pushed to Hugging Face repository.")


if __name__ == "__main__":
    args = parse_args()
    configs_dict = read_yaml(yaml_path=args.configs_path)
    configs = Configs(**configs_dict)
    create(configs=configs)
