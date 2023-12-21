import requests
from typing import Dict
import datetime
import os

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
        "date": date,
        "content": content
    }

    # Convert date to string if it's a date object
    if isinstance(date, datetime.date):
        date = date.isoformat()
    
    response = requests.post(url, headers=headers, params=params, json=data)
    
    if response.ok:
        return response.json()
    else:
        response.raise_for_status()
