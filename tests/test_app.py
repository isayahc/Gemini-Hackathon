import json
import pytest
from unittest.mock import mock_open, patch
from src.Utils.utils import save_to_json  # Replace 'your_module' with the name of your module

@pytest.fixture
def mock_file_open():
    with patch('builtins.open', mock_open()) as mock_file:
        yield mock_file

def test_save_to_json(mock_file_open):
    # Test data and file path
    data = [{"name": "Test", "age": 123}]
    file_path = 'test.json'

    # Call the function
    save_to_json(data, file_path)

    # Check that open was called correctly
    mock_file_open.assert_called_with(file_path, 'w')

    # Serialize data as it would be in json.dump
    serialized_data = json.dumps(data, indent=4)

    # Check that the correct data was written to the file
    mock_file_open().write.assert_called_once_with(serialized_data)

# Run the tests with pytest from the command line
# pytest test_your_module.py
