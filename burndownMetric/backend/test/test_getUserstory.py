import pytest
from unittest.mock import Mock, patch

import requests
from model import mock_userstory_data, mock_custom_attributes_data, mock_custom_attribute_type_bv_id, mock_userstory_by_sprint_id
from taigaApi.userStory.getUserStory import UserStoryFetchingError, get_user_story, get_custom_attribute_from_userstory, get_custom_attribute_type_id, get_userstories_by_sprint
import os
import json



@pytest.fixture() 
def mock_env():
    with patch.dict("os.environ", {"TAIGA_URL": "https://test.taiga.io/api/v1/"}):
        yield

def test_get_user_story_success(mock_env):
    # Set up test data
    
    with patch("requests.get") as mock_get:    

        mock_get.return_value.json.return_value = mock_userstory_data
        # Call the function with mocked data
        user_stories = get_user_story( 1525740, "valid_auth_token")

        # Assert the expected behavior
        assert user_stories == mock_userstory_data


def test_get_user_story_error_connection(mock_env):
    # Simulate a connection error
    with patch("requests.get") as mock_get:
        mock_get.side_effect = requests.exceptions.ConnectionError("Connection error")

        # Call the function
        with pytest.raises(UserStoryFetchingError) as result:
            get_user_story(1525740, "valid_token")

        # Assert expected behavior
        assert result.type is UserStoryFetchingError
        assert result.value.status_code == "CONNECTION_ERROR"
        assert "Connection error" in result.value.reason

def test_get_user_story_error_unauthorized(mock_env):
    # Simulate a connection error
    with patch("requests.get") as mock_get:
        mock_get.side_effect = UserStoryFetchingError(401, "Client Error: Unauthorized")

        # Call the function
        with pytest.raises(UserStoryFetchingError) as result:
            get_user_story(1525740, "invalid_token")

        # Assert expected behavior
        assert result.type is UserStoryFetchingError
        assert result.value.status_code == 401
        assert "Client Error: Unauthorized" in result.value.reason



def test_get_custom_attribute_from_userstory_success(mock_env):
    with patch("requests.get") as mock_get:    

        mock_get.return_value.json.return_value = mock_custom_attributes_data.data
        # Call the function with mocked data
        user_stories = get_custom_attribute_from_userstory(5468297, "valid_auth_token")

        # Assert the expected behavior
        assert user_stories == mock_custom_attributes_data.data['attributes_values'] 


def test_get_custom_attribute_from_userstory_error_connection(mock_env):
    with patch("requests.get") as mock_get:
        mock_get.side_effect = requests.exceptions.ConnectionError("Connection error")

        # Call the function
        with pytest.raises(UserStoryFetchingError) as result:
            get_custom_attribute_from_userstory(5468297, "valid_token")

        # Assert expected behavior
        assert result.type is UserStoryFetchingError
        assert result.value.status_code == "CONNECTION_ERROR"
        assert "Connection error" in result.value.reason

def test_get_custom_attribute_type_id_success(mock_env):
    with patch("requests.get") as mock_get:    

        mock_get.return_value.json.return_value = mock_custom_attribute_type_bv_id.data
        # Call the function with mocked data
        user_stories = get_custom_attribute_type_id(1521718, "valid_auth_token", "BV")

        # Assert the expected behavior
        assert user_stories == str(mock_custom_attribute_type_bv_id.data[0]['id'])

def test_get_custom_attribute_from_userstory_error_unauthorized(mock_env):
    with patch("requests.get") as mock_get:
        mock_get.side_effect = UserStoryFetchingError(401, "Client Error: Unauthorized")

        # Call the function
        with pytest.raises(UserStoryFetchingError) as result:
            get_custom_attribute_from_userstory(5468297, "valid_token")

        # Assert expected behavior
        assert result.type is UserStoryFetchingError
        assert result.value.status_code == 401
        assert "Client Error: Unauthorized" in result.value.reason

def test_get_custom_attribute_type_id_error_connection(mock_env):
    with patch("requests.get") as mock_get:
        mock_get.side_effect = requests.exceptions.ConnectionError("Connection error")

        # Call the function
        with pytest.raises(UserStoryFetchingError) as result:
            get_custom_attribute_type_id(1521718, "valid_token","BV")

        # Assert expected behavior
        assert result.type is UserStoryFetchingError
        assert result.value.status_code == "CONNECTION_ERROR"
        assert "Connection error" in result.value.reason

def test_get_custom_attribute_type_id_error_unauthorized(mock_env):
    with patch("requests.get") as mock_get:
        mock_get.side_effect = UserStoryFetchingError(401, "Client Error: Unauthorized")

        # Call the function
        with pytest.raises(UserStoryFetchingError) as result:
            get_custom_attribute_type_id(123, "invalid_token","BV")

        # Assert expected behavior
        assert result.type is UserStoryFetchingError
        assert result.value.status_code == 401
        assert "Client Error: Unauthorized" in result.value.reason

def test_get_userstories_by_sprint_success(mock_env):
    with patch("requests.get") as mock_get:    

        mock_get.return_value.json.return_value = mock_userstory_by_sprint_id.data
        # Call the function with mocked data
        user_stories = get_userstories_by_sprint(123, "valid_token")

        # Assert the expected behavior
        assert user_stories == mock_userstory_by_sprint_id.data

def test_get_userstories_by_sprint_error_connection(mock_env):
    with patch("requests.get") as mock_get:
        mock_get.side_effect = requests.exceptions.ConnectionError("Connection error")

        # Call the function
        with pytest.raises(UserStoryFetchingError) as result:
            get_userstories_by_sprint(123, "valid_token")

        # Assert expected behavior
        assert result.type is UserStoryFetchingError
        assert result.value.status_code == "CONNECTION_ERROR"
        assert "Connection error" in result.value.reason

def test_get_userstories_by_sprint_error_unauthorized(mock_env):
      with patch("requests.get") as mock_get:
        mock_get.side_effect = UserStoryFetchingError(401, "Client Error: Unauthorized")

        # Call the function
        with pytest.raises(UserStoryFetchingError) as result:
            get_userstories_by_sprint(123, "invalid_token")

        # Assert expected behavior
        assert result.type is UserStoryFetchingError
        assert result.value.status_code == 401
        assert "Client Error: Unauthorized" in result.value.reason
