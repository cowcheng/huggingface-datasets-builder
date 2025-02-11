from datasets.features import Audio, Image

# Mapping of data types to their corresponding feature representations
DATA_TYPE_MAP = {
    "audio": Audio(),  # Represents audio data using the `Audio` feature from the `datasets` library
    "image": Image(),  # Represents image data using the `Image` feature from the `datasets` library
}
