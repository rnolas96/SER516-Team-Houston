import pytest
from service.userstory_service import get_storypoint_burndown_for_sprint, get_partial_storypoint_burndown_for_sprint
from unittest.mock import patch
from model import mock_task_data, mock_module_data


@pytest.mark.parametrize("sprint_id, auth_token, expected_output", [
    # Test case 1: Test with a valid sprint ID
    (376612, "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzA4MjEwMzE5LCJqdGkiOiIxNGE4NzcwMGU5ODg0ZjU4ODZmZWU0N2E0ZDFkNDdjZSIsInVzZXJfaWQiOjYxODc2MX0.AyYr7Cii9nXInz85JzDfWviZT7yc7FlXneOrT5mqNYSY9EgjscOblcWP0PZ5p-TzNg1VPVvnCd4kJn2D5JrEmf5DTTtBlEPUNDJ0SNwjMghQ4Wfo7pMKMKRajJlRhOmfyUVGc6NeRrrpm1OftRBxswh8xI1Ww6JY8U2YK-ZZPpu6366jvJPBUt2MsM4KfkE5GPEKAuICvKE7zirlsMCe01OLOP_TdfYyoaChHVdOlohMvcpr9hZAmXIOI1Ei0cAjRCz1UY0bd_5Miy0Dksx3a3rOk_GGqngXivxXHKbVYkECuJn7A58zm6TJVVGPtIATpzudNV8i_D9Xiu6KZR1CRg",
     {
    "2024-01-29": 48.0,
    "2024-01-30": 48.0,
    "2024-01-31": 48.0,
    "2024-02-01": 48.0,
    "2024-02-02": 48.0,
    "2024-02-03": 48.0,
    "2024-02-04": 48.0,
    "2024-02-05": 48.0,
    "2024-02-06": 48.0,
    "2024-02-07": 48.0,
    "2024-02-08": 48.0,
    "2024-02-09": 48.0,
    "2024-02-10": 48.0,
    "2024-02-11": 48.0,
    "2024-02-12": 32.0,
    "2024-02-13": 32.0,
    "2024-02-14": 32.0,
    "2024-02-15": 31.0,
    "2024-02-16": 31.0,
    "2024-02-17": 31.0,
    "2024-02-18": 31.0
}

    ),

])


def test_storypoint_burndown_for_sprint(sprint_id, auth_token, expected_output):

    mock_response = {
    "2024-01-29": 48.0,
    "2024-01-30": 48.0,
    "2024-01-31": 48.0,
    "2024-02-01": 48.0,
    "2024-02-02": 48.0,
    "2024-02-03": 48.0,
    "2024-02-04": 48.0,
    "2024-02-05": 48.0,
    "2024-02-06": 48.0,
    "2024-02-07": 48.0,
    "2024-02-08": 48.0,
    "2024-02-09": 48.0,
    "2024-02-10": 48.0,
    "2024-02-11": 48.0,
    "2024-02-12": 32.0,
    "2024-02-13": 32.0,
    "2024-02-14": 32.0,
    "2024-02-15": 31.0,
    "2024-02-16": 31.0,
    "2024-02-17": 31.0,
    "2024-02-18": 31.0
}
   
    
    #to mock the http.get request 
    with patch('taigaApi.milestone.getMilestoneById') as mock_get_milestone_by_id:
      mock_sprint_data = mock_module_data.data
      
    mock_get_milestone_by_id.return_value = mock_sprint_data

    with patch('requests.get') as mock_get:
       
      
        mock_get.return_value.json.return_value = mock_sprint_data


        result = get_storypoint_burndown_for_sprint(sprint_id, auth_token)

        assert result == expected_output



@pytest.mark.parametrize("sprint_id, auth_token, expected_output", [
    # Test case 1: Test with a valid sprint ID
    (376612, "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzA4MjIzMTY4LCJqdGkiOiIwY2RlZmZjMzBjMWE0NDI0YWFhZWNlNDhlYzAyM2MxZSIsInVzZXJfaWQiOjYxODc2MX0.jt3DQDUp2rbs9CCThw5dbYKkZ-f4t2oYBEs1LIS2Z37aMO4n4m90HS9Lp7QYcLwEuuqitiDdKSKTw7L4zhTpgtIvemcffNsLT0Ais8ECUZie4dDdfxcB_edwkjiebkbNRU7J5EecHfYUJIF9fC4FjgbKhByh8YQKBOU1MOq9CBgdQmwkrKSgUTUEaefF19f4ZLajq4bNSb862EvMnIDFQeHYnlNGvSEUsiAUGbGjvuXXylJL36nYxZVb7K_QBUqSsRRuODrcZxJro_GawgQ-ui-OHyuu6BjxufMYUdRLVeQ3W_DwRti2SGisNoxIrIV7c5XcTKzroWQtg2g-VW4Qjg",
    {
    "2024-01-29": 48.0,
    "2024-01-30": 48.0,
    "2024-01-31": 48.0,
    "2024-02-01": 48.0,
    "2024-02-02": 48.0,
    "2024-02-03": 48.0,
    "2024-02-04": 48.0,
    "2024-02-05": 44.0,
    "2024-02-06": 43.0,
    "2024-02-07": 40.333333333333336,
    "2024-02-08": 40.333333333333336,
    "2024-02-09": 33.00000000000001,
    "2024-02-10": 33.00000000000001,
    "2024-02-11": 33.00000000000001,
    "2024-02-12": 13.33333333333334,
    "2024-02-13": 13.33333333333334,
    "2024-02-14": 12.33333333333334,
    "2024-02-15": 11.33333333333334,
    "2024-02-16": 11.33333333333334,
    "2024-02-17": 11.33333333333334,
    "2024-02-18": 11.33333333333334
}),

])

def test_get_partial_storypoint_burndown_for_sprint(sprint_id, auth_token,expected_output):


    mock_data=  {
    "2024-01-29": 48.0,
    "2024-01-30": 48.0,
    "2024-01-31": 48.0,
    "2024-02-01": 48.0,
    "2024-02-02": 48.0,
    "2024-02-03": 48.0,
    "2024-02-04": 48.0,
    "2024-02-05": 44.0,
    "2024-02-06": 43.0,
    "2024-02-07": 40.333333333333336,
    "2024-02-08": 40.333333333333336,
    "2024-02-09": 33.00000000000001,
    "2024-02-10": 33.00000000000001,
    "2024-02-11": 33.00000000000001,
    "2024-02-12": 13.33333333333334,
    "2024-02-13": 13.33333333333334,
    "2024-02-14": 12.33333333333334,
    "2024-02-15": 11.33333333333334,
    "2024-02-16": 11.33333333333334,
    "2024-02-17": 11.33333333333334,
    "2024-02-18": 11.33333333333334
}

    #to mock the http.get request 
    with patch('taigaApi.milestone.getMilestoneById.get_milestone_by_id') as mock_get_milestone_by_id,\
        patch('taigaApi.task.getTasks.get_tasks_by_milestone') as mock_get_tasks_by_milestone:

        mock_get_milestone_by_id.return_value = mock_module_data.data
        mock_get_tasks_by_milestone.return_value = mock_task_data.data



        result = get_partial_storypoint_burndown_for_sprint(sprint_id, auth_token)

        assert result == expected_output
