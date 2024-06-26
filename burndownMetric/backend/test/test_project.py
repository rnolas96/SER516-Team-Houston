import pytest
from unittest.mock import Mock, patch
import requests

from model import mock_project_data_by_slug, mock_status_of_tasks_for_project
from taigaApi.project.getProjectBySlug import ProjectFetchingError, get_project_by_slug
from taigaApi.project.getProjectTaskStatusName import TaskStatusFetchError, get_project_task_status_name

@pytest.fixture() 
def mock_env():
    with patch.dict("os.environ", {"TAIGA_URL": "https://test.taiga.io/api/v1/"}):
        yield

def test_get_project_by_slug_success(mock_env):
    project_slug ="rnolas96-taiga-metrics-tool-testing-project-team-houston" 
    auth_token = "valid_auth_token"

    with patch("requests.get") as mock_get:         

        mock_get.return_value.json.return_value = mock_project_data_by_slug.data

         # Call the function with mocked data
        project = get_project_by_slug(project_slug, auth_token)
        # Assert the expected behavior
        assert project == mock_project_data_by_slug.data


def test_get_project_by_project_slug_connection_error(mock_env):
    project_slug ="rnolas96-taiga-metrics-tool-testing-project-team-houston" 
    auth_token = "valid_token"
    # Simulate a connection error
    with patch("requests.get") as mock_get:
        mock_get.side_effect = requests.exceptions.ConnectionError("Connection error")

        # Call the function
        with pytest.raises(ProjectFetchingError) as result:
            get_project_by_slug(project_slug, auth_token)

        # Assert expected behavior
        assert result.type is ProjectFetchingError
        assert result.value.status_code == "CONNECTION_ERROR"
        assert "Connection error" in result.value.reason




def test_get_project_by_project_slug_unauthorized_error(mock_env):
    project_slug ="rnolas96-taiga-metrics-tool-testing-project-team-houston" 
    auth_token = "valid_token"
    # Simulate a connection error
    with patch("requests.get") as mock_get:
        mock_get.side_effect = ProjectFetchingError(401, "Client Error: Unauthorized")

        # Call the function
        with pytest.raises(ProjectFetchingError) as result:
            get_project_by_slug(project_slug, auth_token)

        # Assert expected behavior
        assert result.type is ProjectFetchingError
        assert result.value.status_code == 401
        assert "Client Error: Unauthorized" in result.value.reason


def test_get_project_task_status_name_success(mock_env):
    project_id = 1525740
    auth_token = "valid_auth_token"

    with patch("requests.get") as mock_get:
        mock_get.return_value.json.return_value =  mock_status_of_tasks_for_project.data

        # Call the function with mocked data
        result = get_project_task_status_name(project_id, auth_token)

        #assert the expected result with actual result
        assert result == mock_status_of_tasks_for_project.data



def test_get_project_by_project_slug_connection_error(mock_env):
    project_id = 1525740
    auth_token = "valid_token"
    # Simulate a connection error
    with patch("requests.get") as mock_get:
        mock_get.side_effect = requests.exceptions.ConnectionError("Connection error")

        # Call the function
        with pytest.raises(TaskStatusFetchError) as result:
            get_project_task_status_name(project_id, auth_token)

        # Assert expected behavior
        assert result.type is TaskStatusFetchError
        assert result.value.status_code == "CONNECTION_ERROR"
        assert "Connection error" in result.value.reason





def test_get_project_by_project_slug_unauthorized_error(mock_env):
    project_id = 1525740
    auth_token = "valid_token"
    # Simulate a connection error
    with patch("requests.get") as mock_get:
        mock_get.side_effect = TaskStatusFetchError(401, "Client Error: Unauthorized")

        # Call the function
        with pytest.raises(TaskStatusFetchError) as result:
            get_project_task_status_name(project_id, auth_token)

        # Assert expected behavior
        assert result.type is TaskStatusFetchError
        assert result.value.status_code == 401
        assert "Client Error: Unauthorized" in result.value.reason