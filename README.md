# 📂 HuggingFace Datasets Builder

A powerful and intuitive tool designed to simplify the creation, management, and uploading of datasets to the Hugging Face Hub. With support for various data types including text, audio, and in the future, images and videos, it automates metadata handling and ensures compatibility across multiple dataset formats, making data preparation more efficient.

## 🔄 Features

- **Versatile Data Handling**: Seamlessly supports text, audio, and upcoming support for images and videos.
- **One-Command Hub Upload**: Upload datasets instantly to the Hugging Face Hub with a single command.
- **Flexible Metadata Management**: Easily structure and modify dataset fields, including various metadata types.
- **Config-Driven Customization**: Leverage a YAML-based configuration for streamlined dataset and upload settings.

## 🛠️ Requirements

- **Python 3.11+**

## 📦 Installation

```bash
git clone https://github.com/cowcheng/huggingface-datasets-builder.git
cd huggingface-dataset-builder

python3.11 -m venv .venv
source .venv/bin/activate

pip install -U pip wheel setuptools
pip install -r requirements.txt
```

## 📑 Usage

### 🗃️ Configuration File

Before running the tool, ensure you have a properly configured configs.yaml file. Refer to the sample configuration file located at configs/asr_datasets_sample.yaml. Example configuration:

```yaml
# Dataset configurations
dataset:
  annotation_path: "./common_voice/cantonese.tsv" # Path to the annotation TSV file
  dataframe_order: # Order of columns in the dataset
    - "id"
    - "audio"
    - "raw_transcription"
    - "num_samples"
    - "gender"
    - "lang_id"
    - "language"
    - "lang_group_id"
  cast_columns: # Data type casting for each column
    id: "str"
    audio: "audio"
    raw_transcription: "str"
    num_samples: "str"
    gender: "str"
    lang_id: "str"
    language: "str"
    lang_group_id: "str"
  split: "data" # Dataset split (e.g., train, test)

# Hugging Face Hub configurations
huggingface:
  repo_id: "cowcheng/test" # Your Hugging Face dataset repository ID
  config_name: "cantonese" # Configuration name
  commit_message: "create dataset" # Commit message for uploads
  private: true # Whether the dataset is private
```

### 💡 Running the Tool

```bash
python main.py -c configs.yaml
```

## 👨‍💻 Contributing

Contributions are welcome! Fork the repository, create a branch, and submit a pull request.

## 📚 License

This project is licensed under the MIT License.

## 🎉 Acknowledgments

Special thanks to the open-source community for their invaluable tools and resources.

> For more details, visit the Hugging Face Hub.
