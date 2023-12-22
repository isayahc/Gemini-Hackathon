import requests
from typing import Dict
import datetime
import os
import uuid

def get_entries(email: str, api_key: str) -> Dict:
    url = f"{os.getenv('API_DOMAIN')}/api/v1/get-entries"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36"
    }
    params = {
        "email": email,
        "api_key": api_key
    }
    
    response = requests.get(url, headers=headers, params=params)
    
    if response.ok:
        return response.json()
    else:
        response.raise_for_status()


# def add_entry(email: str, api_key: str, date: str, content: str) -> Dict:
#     url = f"{os.getenv('API_DOMAIN')}/api/v1/add-entry"
#     headers = {
#         "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36"
#     }
#     params = {
#         "email": email,
#         "api_key": api_key
#     }
#     data = {
#         "date": date,
#         "content": content
#     }

#     # Convert date to string if it's a date object
#     if isinstance(date, datetime.date):
#         date = date.isoformat()
    
#     response = requests.post(url, headers=headers, params=params, json=data)
    
#     if response.ok:
#         return response.json()
#     else:
#         response.raise_for_status()



def delete_entry(email: str, api_key: str, entry_id: str) -> Dict:
    """
    Deletes an entry from the server.

    Parameters:
    - email (str): The email address associated with the entry.
    - api_key (str): The API key for authentication.
    - entry_id (str): The unique identifier for the entry to delete.

    Returns:
    - Dict: The JSON response from the server.
    """
    url = f"{os.getenv('API_DOMAIN')}/api/v1/delete-entry/{entry_id}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36"
    }
    params = {
        "email": email,
        "api_key": api_key
    }
    
    response = requests.delete(url, headers=headers, params=params)
    
    if response.ok:
        return response.json()
    else:
        response.raise_for_status()

def add_entry(email: str, api_key: str, date: str, content: str) -> Dict:
    url = f"{os.getenv('API_DOMAIN')}/api/v1/add-entry"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36"
    }
    params = {
        "email": email,
        "api_key": api_key
    }
    data = {
        "id": str(uuid.uuid4()),  # Generate a new UUID for each entry
        "date": date,
        "content": content
    }

    # Convert date to string if it's a date object
    if isinstance(date, datetime.date):
        data["date"] = date.isoformat()
    
    response = requests.post(url, headers=headers, params=params, json=data)
    
    if response.ok:
        return response.json()
    else:
        response.raise_for_status()

