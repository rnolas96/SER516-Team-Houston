import pytest
from unittest.mock import Mock, patch

import requests
from model import mock_task_data, mock_closed_tasks, mock_tasks_by_milestone
from taigaApi.task.getTasks import TaskFetchingError, get_tasks, get_closed_tasks, get_tasks_by_milestone


@pytest.fixture() 
def mock_env():
    with patch.dict("os.environ", {"TAIGA_URL": "https://test.taiga.io/api/v1/"}):
        yield

def test_get_tasks(mock_env):
    
    project_id = 1522285
    auth_token = "valid_auth_token"
    
    with patch("requests.get") as mock_get:         

        mock_get.return_value.json.return_value = mock_task_data.data

         # Call the function with mocked data
        tasks = get_tasks( project_id,auth_token)

        # Assert the expected behavior
        assert tasks == mock_task_data.data


def test_get_all_tasks_connection_error(mock_env):
    project_id = 1522285
    auth_token = "valid_token"
    # Simulate a connection error
    with patch("requests.get") as mock_get:
        mock_get.side_effect = requests.exceptions.ConnectionError("Connection error")

        # Call the function
        with pytest.raises(TaskFetchingError) as result:
            get_tasks(project_id, auth_token)

        # Assert expected behavior
        assert result.type is TaskFetchingError
        assert result.value.status_code == "CONNECTION_ERROR"
        assert "Connection error" in result.value.reason

def test_get_tasks_error_unauthorized(mock_env):
    project_id = 1522285
    auth_token = "invalid_token"
    # Simulate a connection error
    with patch("requests.get") as mock_get:
        mock_get.side_effect = TaskFetchingError(401, "Client Error: Unauthorized")

        # Call the function
        with pytest.raises(TaskFetchingError) as result:
            get_tasks(project_id, auth_token)

        print("result------------",result.type)
        # Assert expected behavior
        assert result.type is TaskFetchingError
        assert result.value.status_code == 401
        assert "Client Error: Unauthorized" in result.value.reason

    



def test_tasks_by_milestone_success(mock_env):
    
    project_id = 1521718
    sprint_id=376612
    auth_token = "valid_auth_token"
    
    with patch("requests.get") as mock_get:         

        mock_get.return_value.json.return_value = mock_tasks_by_milestone.data

         # Call the function with mocked data
        tasks_by_milestone = get_tasks_by_milestone(project_id, sprint_id, auth_token)

        # Assert the expected behavior
        assert tasks_by_milestone == mock_tasks_by_milestone.data



def test_tasks_by_milestone_connection_error(mock_env):
    project_id = 1521718
    sprint_id=376612
    auth_token = "valid_auth_token"

    with patch("requests.get") as mock_get:
        mock_get.side_effect = requests.exceptions.ConnectionError("Connection error")

        # Call the function
        with pytest.raises(TaskFetchingError) as result:
            get_tasks_by_milestone(project_id, sprint_id, auth_token)

        # Assert expected behavior
        assert result.type is TaskFetchingError
        assert result.value.status_code == "CONNECTION_ERROR"
        assert "Connection error" in result.value.reason



def test_tasks_by_milestone_authorization_error(mock_env):
    project_id = 1521718
    sprint_id=376612
    auth_token = "valid_auth_token"

    # Simulate a 401 Unauthorized error
    with patch("requests.get") as mock_get:
        mock_get.side_effect = TaskFetchingError(401, "Client Error: Unauthorized")

        # Call the function
        with pytest.raises(TaskFetchingError) as result:
            get_tasks_by_milestone(project_id, sprint_id, auth_token)

        # Assert expected behavior
        assert result.type is TaskFetchingError
        assert result.value.status_code == 401
        assert "Client Error: Unauthorized" in result.value.reason


