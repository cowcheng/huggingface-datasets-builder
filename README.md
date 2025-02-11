# 🤖 HuggingFace Datasets Builder

A robust and user-friendly tool for creating, managing, and uploading datasets to the Hugging Face Hub. Designed with seamless support for audio datasets, it simplifies metadata handling and ensures compatibility with various dataset formats, streamlining data preparation.

## 🚀 Features

- **Universal Format Support**: Seamlessly handle text and audio datasets with built-in adaptability.
  > Future updates will include support for images and videos.
- **Automated Data Transformation**: Convert raw data into Hugging Face-compatible datasets without manual intervention.
- **Effortless Hub Integration**: Instantly upload datasets to the Hugging Face Hub with a single command.
- **Dynamic Metadata Handling**: Easily manage and customize dataset fields, including audio, transcriptions, and metadata.
- **YAML-Based Configuration**: Modify dataset settings and upload parameters effortlessly using a structured configuration file.

## 📋 Requirements

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

## 🛠️ Usage

### 📝 Configuration File

Before running the tool, ensure you have a properly configured `configs.yaml` file. Example configuration:

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

### 📂 Running the Tool

```bash
python main.py -c configs.yaml
```

## 🤝 Contributing

Contributions are welcome! Fork the repository, create a branch, and submit a pull request.

## 📜 License

This project is licensed under the MIT License.

## 🙌 Acknowledgments

Special thanks to the open-source community for their invaluable tools and resources.

> For more details, visit the Hugging Face Hub.
