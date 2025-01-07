# 🤖 Hugging Face Dataset Tool

An all-in-one solution for efficiently creating, managing, and uploading datasets to the Hugging Face Hub. Designed with robust support for audio datasets, it simplifies metadata handling and ensures seamless integration with diverse dataset formats.

## 🚀 Features

- **Multi-format Compatibility**: Effortlessly handle text, audio, image, and video datasets without additional configuration.
- **Seamless Data Conversion**: Automatically convert raw data into Hugging Face-compatible datasets.
- **One-Click Upload**: Direct integration with the Hugging Face Hub for quick and reliable dataset uploads.
- **Dynamic Data Processing**: Flexibly manage fields such as audio content, transcriptions, and rich metadata.
- **Config-Driven Workflow**: Simplify dataset customization and upload parameters using easy-to-edit YAML files.

## 📋 Requirements

- **Python 3.11+**

## 📦 Installation

```bash
git clone https://github.com/yourusername/huggingface-dataset-builder.git
cd huggingface-dataset-builder

python3.11 -m venv .venv
source .venv/bin/activate

pip install -U pip wheel setuptools
pip install -r requirements.txt
```

## 🛠️ Usage

### 📑 Configuration File

Before running the tool, ensure you have a properly configured config.yaml file. Below is an example configuration:

```yaml
# Dataset configuration
dataset:
  annotation_path: "./google_fleurs_v1/cantonese.csv" # Path to the annotation CSV file
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

# Hugging Face Hub configuration
huggingface:
  repo_id: "cowcheng/test" # Your Hugging Face dataset repository ID
  config_name: "cantonese" # Configuration name
  commit_message: "create dataset" # Commit message for uploads
  private: true # Whether the dataset is private
  revision: "main" # Dataset revision branch
```

### 📂 Run the Tool

```bash
python main.py -c config.yaml
```

## 🤝 Contributing

Contributions are welcome! Please fork the repository, create a branch, and submit a pull request.

## 📜 License

This project is licensed under the MIT License.

## 🙌 Acknowledgments

Special thanks to the Hugging Face team and the open-source community for their amazing tools and resources.

> For more information, visit the Hugging Face Hub.
