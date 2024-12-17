from datasets.features import Audio, Image, Video

"""
Dictionary mapping media type strings to their corresponding Hugging Face dataset feature objects.
This mapping is used to specify the correct feature type when creating or processing datasets
containing media files.

The following feature types are supported:
  - "audio": For audio files (e.g., wav, mp3, flac)
  - "image": For image files (e.g., jpg, png, bmp)
  - "video": For video files (e.g., mp4, avi, mov)

Each feature type handles decoding, loading, and processing of the corresponding media type
according to Hugging Face datasets specifications.

Example:
  ```python
  from datasets import Features
  
  Creating features dictionary for a dataset with image and audio
  features = Features({
      "image_path": DATA_TYPE_MAP["image"],
      "audio_path": DATA_TYPE_MAP["audio"],
      "label": "int64"
  })
  ```
"""
DATA_TYPE_MAP = {
    "audio": Audio(),
    "image": Image(),
    "video": Video(),
}
