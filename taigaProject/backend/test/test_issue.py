import pytest
from unittest.mock import Mock, patch
import requests
from taigaApi.issue.getIssuesByProjectId import IssueFetchingError, get_issues_by_project_id
from taigaApi.issue.getCustomAttributeValueByIssueId import CustomeAttributeFetchingError, get_custom_attribute_type_id_for_issue, get_custom_attribute_value_by_issue_id

from model import mock_issue_custom_attributes_by_project_id, mock_issues, mock_custom_attribute_info


@pytest.fixture() 
def mock_env():
    with patch.dict("os.environ", {"TAIGA_URL": "https://test.taiga.io/api/v1/"}):
        yield


def test_get_issues_by_project_id_success(mock_env):
    project_id = 1521718
    auth_token = "valid_auth_token"

    with patch("requests.get") as mock_get:         

        mock_get.return_value.json.return_value = mock_issues.data

         # Call the function with mocked data
        issues = get_issues_by_project_id(project_id, auth_token)

        # Assert the expected behavior
        assert issues == mock_issues.data



def test_get_issues_by_project_id_connection_error(mock_env):
    project_id = 1521718
    auth_token = "valid_token"
    # Simulate a connection error
    with patch("requests.get") as mock_get:
        mock_get.side_effect = requests.exceptions.ConnectionError("Connection error")

        # Call the function
        with pytest.raises(IssueFetchingError) as result:
            get_issues_by_project_id(project_id, auth_token)

        # Assert expected behavior
        assert result.type is IssueFetchingError
        assert result.value.status_code == "CONNECTION_ERROR"
        assert "Connection error" in result.value.reason



def test_get_tasks_error_unauthorized(mock_env):
    project_id = 1521718
    auth_token = "invalid_token"
    # Simulate a connection error
    with patch("requests.get") as mock_get:
        mock_get.side_effect = IssueFetchingError(401, "Client Error: Unauthorized")

        # Call the function
        with pytest.raises(IssueFetchingError) as result:
            get_issues_by_project_id(project_id, auth_token)

        # Assert expected behavior
        assert result.type is IssueFetchingError
        assert result.value.status_code == 401
        assert "Client Error: Unauthorized" in result.value.reason




def test_get_custom_attribute_type_id_for_issue_success(mock_env):
        project_id = 1525740
        attribute_name = 'blocked'
        auth_token = "valid_auth_token"

        custom_attribute_type_id = '18181'


        with patch("requests.get") as mock_get:         

            mock_get.return_value.json.return_value = mock_issue_custom_attributes_by_project_id.data

            # Call the function with mocked data
            issues = get_custom_attribute_type_id_for_issue(project_id, auth_token, attribute_name)

            # Assert the expected behavior
            assert issues == custom_attribute_type_id


def test_get_custom_attribute_type_id_for_issue_connection_error(mock_env):
    project_id = 1525740
    attribute_name = 'blocked'
    auth_token = "valid_auth_token" 

    # Simulate a connection error
    with patch("requests.get") as mock_get:
        mock_get.side_effect = requests.exceptions.ConnectionError("Connection error")

        # Call the function
        with pytest.raises(CustomeAttributeFetchingError) as result:
            get_custom_attribute_type_id_for_issue(project_id, auth_token, attribute_name)

        # Assert expected behavior
        assert result.type is CustomeAttributeFetchingError
        assert result.value.status_code == "CONNECTION_ERROR"
        assert "Connection error" in result.value.reason




def test_get_custom_attribute_type_id_for_issue_error_unauthorized(mock_env):
    project_id = 1525740
    attribute_name = 'blocked'
    auth_token = "invalid_token"

    # Simulate a connection error
    with patch("requests.get") as mock_get:
        mock_get.side_effect = CustomeAttributeFetchingError(401, "Client Error: Unauthorized")

        # Call the function
        with pytest.raises(CustomeAttributeFetchingError) as result:
            get_custom_attribute_type_id_for_issue(project_id, auth_token, attribute_name)
        # Assert expected behavior
        assert result.type is CustomeAttributeFetchingError
        assert result.value.status_code == 401
        assert "Client Error: Unauthorized" in result.value.reason




def test_get_custom_attribute_value_by_issue_id_success(mock_env):
    issue_id = 1729278
    attribute_id = '18181'
    auth_token = "valid_token"

    attribute_value = '#5'

    with patch("requests.get") as mock_get:         

            mock_get.return_value.json.return_value = mock_custom_attribute_info.data

            # Call the function with mocked data
            issues = get_custom_attribute_value_by_issue_id(issue_id, attribute_id, auth_token)

            # Assert the expected behavior
            assert issues == attribute_value

def test_get_custom_attribute_value_by_issue_id_connection_error(mock_env):
    issue_id = 1729278
    attribute_id = '18181'
    auth_token = "valid_token"

    # Simulate a connection error
    with patch("requests.get") as mock_get:
        mock_get.side_effect = requests.exceptions.ConnectionError("Connection error")

        # Call the function
        with pytest.raises(CustomeAttributeFetchingError) as result:
            get_custom_attribute_value_by_issue_id(issue_id, attribute_id, auth_token)


        # Assert expected behavior
        assert result.type is CustomeAttributeFetchingError
        assert result.value.status_code == "CONNECTION_ERROR"
        assert "Connection error" in result.value.reason


def test_get_custom_attribute_value_by_issue_id_error_unauthorized(mock_env):
    issue_id = 1729278
    attribute_id = '18181'
    auth_token = "invalid_token"

    # Simulate a connection error
    with patch("requests.get") as mock_get:
        mock_get.side_effect = CustomeAttributeFetchingError(401, "Client Error: Unauthorized")

        # Call the function
        with pytest.raises(CustomeAttributeFetchingError) as result:
             get_custom_attribute_value_by_issue_id(issue_id, attribute_id, auth_token)
        # Assert expected behavior
        assert result.type is CustomeAttributeFetchingError
        assert result.value.status_code == 401
        assert "Client Error: Unauthorized" in result.value.reason
