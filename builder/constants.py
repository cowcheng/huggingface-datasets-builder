from datasets.features import Audio, Image, Video

"""
Mapping of media types to their corresponding processor classes.

Keys are media type strings and values are processor instances that handle
each specific media type's validation and processing logic.
"""
DATA_TYPE_MAP = {
    "audio": Audio(),
    "image": Image(),
    "video": Video(),
}
