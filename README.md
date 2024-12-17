# HuggingFace Dataset Builder

A versatile tool for creating and uploading datasets to the Hugging Face Hub, with special support for handling audio datasets and their associated metadata.

## Features

- **Multi-format Support**: Process various data types including text and audio files
- **Automated Conversion**: Transform raw data into Hugging Face dataset-compatible formats
- **Direct Upload Integration**: Seamlessly push processed datasets to the Hugging Face Hub
- **Flexible Processing**: Support for multiple data fields including audio, transcriptions, and metadata
- **Easy Configuration**: YAML-based configuration for dataset settings and upload parameters

## Installation

```bash
git clone https://github.com/yourusername/huggingface-dataset-builder.git
cd huggingface-dataset-builder

python3.11 -m venv .venv
source .venv/bin/activate

pip install -U pip wheel setuptools
pip install -r requirements.txt
```

## Quick Start

1. Prepare your configuration file (e.g., `config.yaml`):

   ```yaml
   dataset:
     annotation_path: "./data/cantonese.csv"
     dataframe_order:
       - "id"
       - "audio"
       - "raw_transcription"
       - "num_samples"
       - "gender"
       - "lang_id"
       - "language"
       - "lang_group_id"
     cast_columns:
       id: "str"
       audio: "audio"
       raw_transcription: "str"
       num_samples: "str"
       gender: "str"
       lang_id: "str"
       language: "str"
       lang_group_id: "str"
     split: "data"

   huggingface:
     repo_id: "username/repository-name"
     config_name: "cantonese"
     commit_message: "create dataset"
     private: true
     revision: "main"
   ```

2. Run the builder:

   ```bash
   python main.py -c config.yaml
   ```

## Configuration Guide

### Dataset Configuration

| Parameter         | Description                      | Example                                |
| ----------------- | -------------------------------- | -------------------------------------- |
| `annotation_path` | Path to the annotation CSV file  | `"./data/cantonese.csv"`               |
| `dataframe_order` | List of columns in desired order | `["id", "audio", "raw_transcription"]` |
| `cast_columns`    | Column name to data type mapping | `{"audio": "audio", "id": "str"}`      |
| `split`           | Dataset split name               | `"data"` or `"train"`                  |

### Hugging Face Configuration

| Parameter        | Description                | Example                |
| ---------------- | -------------------------- | ---------------------- |
| `repo_id`        | Hugging Face repository ID | `"username/repo-name"` |
| `config_name`    | Configuration name         | `"cantonese"`          |
| `commit_message` | Commit message for upload  | `"create dataset"`     |
| `private`        | Repository privacy setting | `true` or `false`      |
| `revision`       | Repository branch or tag   | `"main"`               |

## Supported Data Types

- **String**: Text data (`"str"`)
- **Audio**: Audio files (`"audio"`)
- **Image**: Image files (`"image"`)
- **Video**: Video files (`"video"`)

## Project Structure

```bash
huggingface-dataset-builder/
├── builder/
│   ├── configs/
│   │   ├── __init__.py
│   │   └── config.py
│   ├── __init__.py
│   ├── constants.py
│   ├── main.py
│   └── utils.py
├── README.md
└── setup.py
```

## Usage Example

### Audio Dataset with Metadata

```yaml
dataset:
  annotation_path: "./data/cantonese.csv"
  dataframe_order:
    - "id"
    - "audio"
    - "raw_transcription"
    - "num_samples"
    - "gender"
    - "lang_id"
    - "language"
    - "lang_group_id"
  cast_columns:
    id: "str"
    audio: "audio"
    raw_transcription: "str"
    num_samples: "str"
    gender: "str"
    lang_id: "str"
    language: "str"
    lang_group_id: "str"
  split: "data"

huggingface:
  repo_id: "username/audio-dataset"
  config_name: "cantonese"
  commit_message: "Upload Cantonese audio dataset"
  private: true
  revision: "main"
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [Hugging Face Datasets](https://github.com/huggingface/datasets)
- [Pandas](https://pandas.pydata.org/)
- [PyYAML](https://pyyaml.org/)

## Contact

For questions and feedback, please open an issue on the GitHub repository.
