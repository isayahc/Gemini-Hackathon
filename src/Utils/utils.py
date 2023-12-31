import json
import logging
from typing import List, Dict
from google.cloud import storage


def save_to_json(data: List[Dict[str, any]], file_path: str) -> None:
    """
    Save a list of dictionaries to a JSON file.

    This function takes a list of dictionaries and writes it to a file in JSON format.
    The output is formatted with an indentation of 4 spaces for better readability.

    Args:
        data (List[Dict[str, any]]): The data to be saved in JSON format.
        file_path (str): The path of the file where the JSON data will be saved.

    Example:
        data = [
            {"name": "Alice", "age": 30, "city": "New York"},
            {"name": "Bob", "age": 25, "city": "Paris"}
        ]
        save_to_json(data, 'data.json')
    """
    try:
        with open(file_path, 'w') as file:
            json.dump(data, file, indent=4)
    except Exception as e:
        logging.info(f"Data successfully saved to {file_path}")

        logging.error(f"Failed to save data to {file_path}: {e}")



def download_blob(
        bucket_name:str,
        source_blob_name:str,
        DESTINATION_FILE_NAME:str
        ) -> None:
    """This function is to download a blob from google bucket
    :param bucket_name : str name of bucket
    :param source_blob : str location of file in the bucket
    :param destination_file_name : str location of disk of where to write file
    
    Keyword arguments:
    argument -- description
    Return: None
    """
    
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(source_blob_name)
    blob.download_to_filename(DESTINATION_FILE_NAME)


