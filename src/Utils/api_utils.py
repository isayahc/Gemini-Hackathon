import requests
from typing import Dict
import datetime
import os
import uuid
from typing import Any

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36"

def get_entries(email: str, api_key: str) -> Dict:
    """
    This function is to get the entries of 

    ## Parameters:
    - email (str): The email address associated with the entry.
    - api_key (str): The API key for authentication.

    ## Returns 
    List[Dict] of journal entries 
    """
    
    url = f"{os.getenv('API_DOMAIN')}/api/v1/get-entries"
    headers = {
        "User-Agent": USER_AGENT
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


def delete_entry(email: str, api_key: str, entry_id: str) -> Dict:
    """
    Deletes an entry from the server.

    ## Parameters:
    - email (str): The email address associated with the entry.
    - api_key (str): The API key for authentication.
    - entry_id (str): The unique identifier for the entry to delete.

    ## Returns:
    - Dict: The JSON response from the server.
    """
    url = f"{os.getenv('API_DOMAIN')}/api/v1/delete-entry/{entry_id}"
    headers = {
        "User-Agent": USER_AGENT
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
    """
    Adds an entry to the database

    ## Parameters:
    - email (str): The email address associated with the entry.
    - api_key (str): The API key for authentication.

    ## Returns:
    - Dict[str, Any]: The JSON response from the server.
    """
    url = f"{os.getenv('API_DOMAIN')}/api/v1/add-entry"
    headers = {
        "User-Agent": USER_AGENT
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


def update_entry(email: str, api_key: str, entry_id: str, date: datetime.date, content: str) -> Dict[str, Any]:
    """
    Updates an existing entry on the server.

    ## Parameters:
    - email (str): The email address associated with the entry.
    - api_key (str): The API key for authentication.
    - entry_id (str): The unique identifier for the entry to update.
    - date (datetime.date): The date of the entry.
    - content (str): The content of the entry.

    ## Returns:
    - Dict[str, Any]: The JSON response from the server.
    """
    url = f"{os.getenv('API_DOMAIN')}/api/v1/update-entry/{entry_id}"
    headers = {
        "User-Agent": USER_AGENT
    }
    params = {
        "email": email,
        "api_key": api_key
    }
    data = {
        "date": date.isoformat() if isinstance(date, datetime.date) else date,
        "content": content
    }
    
    response = requests.put(url, headers=headers, params=params, json=data)
    
    if response.ok:
        return response.json()
    else:
        response.raise_for_status()

def query_entries(email: str, api_key: str, query:str) -> Dict:
    """
    This function is to get the entries of 

    ## Parameters:
    - email (str): The email address associated with the entry.
    - api_key (str): The API key for authentication.
    - query (str): a query for the user

    ## Returns 
    
    """
    url = f"{os.getenv('API_DOMAIN')}/api/v1/entries-queries"
    headers = {
        "User-Agent": USER_AGENT
    }
    params = {
        "email": email,
        "api_key": api_key,
        "query" : query,
    }
    
    response = requests.get(url, headers=headers, params=params)
    
    if response.ok:
        return response.json()
    else:
        response.raise_for_status()