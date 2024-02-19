import pytest
from unittest.mock import patch
from model import mock_task_data, mock_module_data
from taigaApi.task.getTasks import get_tasks_by_milestone
import os
import json

@pytest.mark.parametrize("milestone_id, project_id, auth_token, expected_output", [
    # Test case 1: Test with a valid sprint ID
    (376612, 1521718, "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzA4MzA4NzgyLCJqdGkiOiJjZWE3ZDc1NzlhZmQ0NzA1ODBmODkzZDYxZDdiYTk2MSIsInVzZXJfaWQiOjYxODc2MX0.RwQZAzeLc4MuM5Zz9Z9naCOOwab5iBo_O6aU977eqMPRtFMluyAsSdSUdHydgOH_CkJniQ6SyYYLNtGAhFsdpFkYQZbiGFDgd_iEgIAw7DpTYhewQ8gcpmyC9fi3CtdyoELqmU9zSxfre32EBbB0aXdFu37Tavr5sdBzDelxVa3rEQ1qC1EPhr9jJoZXNZ6RiBn9FXrHu4A1gOOU1Gj9y7M0puXZGGkG0kqt6Oa6EA1QHqks1rw-21KN2QLl2kYBO8hQMowVPULlP8LmwJxdD5vjO9xgPRBeBx-A0VXmBAUXU1bmY73hPWCq-wO4DKM4e8OjVSfnJf7mcts_Mf6wIg",
     mock_task_data.data,
    )
]
)

@patch('taigaApi.task.getTasks.requests.get')
def test_get_task_by_milestone(mock_tasks, milestone_id, project_id, auth_token, expected_output):

    mock_tasks.return_value.json.return_value = mock_task_data.data

    result = get_tasks_by_milestone(milestone_id, project_id, auth_token)
    assert result == expected_output