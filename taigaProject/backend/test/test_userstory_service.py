import pytest
from service.userstory_service import get_storypoint_burndown_for_sprint
from unittest.mock import patch


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
      mock_sprint_data = {
        "project": 1521718,
        "project_extra_info": {
            "name": "SER516-Team-Houston",
            "slug": "ser516asu-ser516-team-houston",
            "logo_small_url": None,
            "id": 1521718
        },
        "id": 376612,
        "name": "Sprint 1",
        "slug": "sprint-1-7317",
        "owner": 501364,
        "estimated_start": "2024-01-29",
        "estimated_finish": "2024-02-18",
        "created_date": "2024-01-29T21:20:04.204Z",
        "modified_date": "2024-02-14T01:35:50.251Z",
        "closed": False,
        "disponibility": 0.0,
        "order": 1,
        "user_stories": [
            {
                "due_date": None,
                "due_date_reason": "",
                "due_date_status": "not_set",
                "assigned_to": None,
                "assigned_to_extra_info": None,
                "status": 9157381,
                "status_extra_info": {
                    "name": "New",
                    "color": "#70728F",
                    "is_closed": False
                },
                "project": 1521718,
                "project_extra_info": {
                    "name": "SER516-Team-Houston",
                    "slug": "ser516asu-ser516-team-houston",
                    "logo_small_url": None,
                    "id": 1521718
                },
                "id": 5468108,
                "ref": 4,
                "milestone": 376612,
                "is_closed": False,
                "created_date": "2024-01-29T21:02:53.914Z",
                "modified_date": "2024-02-14T14:05:50.058Z",
                "finish_date": None,
                "subject": "Select a Taiga project to apply this metric to",
                "client_requirement": False,
                "team_requirement": False,
                "external_reference": None,
                "version": 3,
                "is_blocked": False,
                "blocked_note": "",
                "backlog_order": 1706562173914113,
                "sprint_order": 1,
                "kanban_order": 1706562173914118,
                "epics": [
                    {
                        "id": 218035,
                        "ref": 1,
                        "subject": "Burndown chart",
                        "color": "#5551D3",
                        "project": {
                            "id": 1521718,
                            "name": "SER516-Team-Houston",
                            "slug": "ser516asu-ser516-team-houston"
                        }
                    }
                ],
                "points": {
                    "9184536": 18295632
                },
                "total_points": 1.0
            },
            {
                "due_date": None,
                "due_date_reason": "",
                "due_date_status": "not_set",
                "assigned_to": None,
                "assigned_to_extra_info": None,
                "status": 9157381,
                "status_extra_info": {
                    "name": "New",
                    "color": "#70728F",
                    "is_closed": False
                },
                "project": 1521718,
                "project_extra_info": {
                    "name": "SER516-Team-Houston",
                    "slug": "ser516asu-ser516-team-houston",
                    "logo_small_url": None,
                    "id": 1521718
                },
                "id": 5468114,
                "ref": 5,
                "milestone": 376612,
                "is_closed": False,
                "created_date": "2024-01-29T21:04:15.809Z",
                "modified_date": "2024-02-14T14:06:16.266Z",
                "finish_date": None,
                "subject": "Configure the metric parameters",
                "client_requirement": False,
                "team_requirement": False,
                "external_reference": None,
                "version": 6,
                "is_blocked": False,
                "blocked_note": "",
                "backlog_order": 1706562255809081,
                "sprint_order": 2,
                "kanban_order": 1706562255809086,
                "epics": [
                    {
                        "id": 218035,
                        "ref": 1,
                        "subject": "Burndown chart",
                        "color": "#5551D3",
                        "project": {
                            "id": 1521718,
                            "name": "SER516-Team-Houston",
                            "slug": "ser516asu-ser516-team-houston"
                        }
                    }
                ],
                "points": {
                    "9184536": 18295634
                },
                "total_points": 3.0
            },
            {
                "due_date": None,
                "due_date_reason": "",
                "due_date_status": "not_set",
                "assigned_to": None,
                "assigned_to_extra_info": None,
                "status": 9157381,
                "status_extra_info": {
                    "name": "New",
                    "color": "#70728F",
                    "is_closed": False
                },
                "project": 1521718,
                "project_extra_info": {
                    "name": "SER516-Team-Houston",
                    "slug": "ser516asu-ser516-team-houston",
                    "logo_small_url": None,
                    "id": 1521718
                },
                "id": 5468124,
                "ref": 6,
                "milestone": 376612,
                "is_closed": False,
                "created_date": "2024-01-29T21:05:25.090Z",
                "modified_date": "2024-02-14T14:05:25.854Z",
                "finish_date": None,
                "subject": "Get the data and compute the metric raw value",
                "client_requirement": False,
                "team_requirement": False,
                "external_reference": None,
                "version": 5,
                "is_blocked": False,
                "blocked_note": "",
                "backlog_order": 1706562325090431,
                "sprint_order": 3,
                "kanban_order": 1706562325090436,
                "epics": [
                    {
                        "id": 218035,
                        "ref": 1,
                        "subject": "Burndown chart",
                        "color": "#5551D3",
                        "project": {
                            "id": 1521718,
                            "name": "SER516-Team-Houston",
                            "slug": "ser516asu-ser516-team-houston"
                        }
                    }
                ],
                "points": {
                    "9184536": 18295636
                },
                "total_points": 8.0
            },
            {
                "due_date": None,
                "due_date_reason": "",
                "due_date_status": "not_set",
                "assigned_to": None,
                "assigned_to_extra_info": None,
                "status": 9157381,
                "status_extra_info": {
                    "name": "New",
                    "color": "#70728F",
                    "is_closed": False
                },
                "project": 1521718,
                "project_extra_info": {
                    "name": "SER516-Team-Houston",
                    "slug": "ser516asu-ser516-team-houston",
                    "logo_small_url": None,
                    "id": 1521718
                },
                "id": 5468131,
                "ref": 7,
                "milestone": 376612,
                "is_closed": False,
                "created_date": "2024-01-29T21:06:05.751Z",
                "modified_date": "2024-02-14T14:01:50.274Z",
                "finish_date": None,
                "subject": "Visualize the metric in an appropriate way",
                "client_requirement": False,
                "team_requirement": False,
                "external_reference": None,
                "version": 4,
                "is_blocked": False,
                "blocked_note": "",
                "backlog_order": 1706562365751243,
                "sprint_order": 4,
                "kanban_order": 1706562365751249,
                "epics": [
                    {
                        "id": 218035,
                        "ref": 1,
                        "subject": "Burndown chart",
                        "color": "#5551D3",
                        "project": {
                            "id": 1521718,
                            "name": "SER516-Team-Houston",
                            "slug": "ser516asu-ser516-team-houston"
                        }
                    }
                ],
                "points": {
                    "9184536": 18295636
                },
                "total_points": 8.0
            },
            {
                "due_date": None,
                "due_date_reason": "",
                "due_date_status": "not_set",
                "assigned_to": None,
                "assigned_to_extra_info": None,
                "status": 9157381,
                "status_extra_info": {
                    "name": "New",
                    "color": "#70728F",
                    "is_closed": False
                },
                "project": 1521718,
                "project_extra_info": {
                    "name": "SER516-Team-Houston",
                    "slug": "ser516asu-ser516-team-houston",
                    "logo_small_url": None,
                    "id": 1521718
                },
                "id": 5468154,
                "ref": 8,
                "milestone": 376612,
                "is_closed": True,
                "created_date": "2024-01-29T21:10:13.537Z",
                "modified_date": "2024-02-14T14:03:54.620Z",
                "finish_date": "2024-02-15T23:27:40.685Z",
                "subject": "Select a taiga project to apply it to.",
                "client_requirement": False,
                "team_requirement": False,
                "external_reference": None,
                "version": 2,
                "is_blocked": False,
                "blocked_note": "",
                "backlog_order": 1706562613537284,
                "sprint_order": 5,
                "kanban_order": 1706562613537289,
                "epics": [
                    {
                        "id": 218046,
                        "ref": 2,
                        "subject": "Cycle time",
                        "color": "#A3D350",
                        "project": {
                            "id": 1521718,
                            "name": "SER516-Team-Houston",
                            "slug": "ser516asu-ser516-team-houston"
                        }
                    }
                ],
                "points": {
                    "9184536": 18295632
                },
                "total_points": 1.0
            },
            {
                "due_date": None,
                "due_date_reason": "",
                "due_date_status": "not_set",
                "assigned_to": None,
                "assigned_to_extra_info": None,
                "status": 9157381,
                "status_extra_info": {
                    "name": "New",
                    "color": "#70728F",
                    "is_closed": False
                },
                "project": 1521718,
                "project_extra_info": {
                    "name": "SER516-Team-Houston",
                    "slug": "ser516asu-ser516-team-houston",
                    "logo_small_url": None,
                    "id": 1521718
                },
                "id": 5468155,
                "ref": 9,
                "milestone": 376612,
                "is_closed": True,
                "created_date": "2024-01-29T21:10:13.537Z",
                "modified_date": "2024-02-14T14:06:31.504Z",
                "finish_date": "2024-02-12T06:11:03.060Z",
                "subject": "Configure the metric parameters.",
                "client_requirement": False,
                "team_requirement": False,
                "external_reference": None,
                "version": 4,
                "is_blocked": False,
                "blocked_note": "",
                "backlog_order": 1706562613537372,
                "sprint_order": 6,
                "kanban_order": 1706562613537375,
                "epics": [
                    {
                        "id": 218046,
                        "ref": 2,
                        "subject": "Cycle time",
                        "color": "#A3D350",
                        "project": {
                            "id": 1521718,
                            "name": "SER516-Team-Houston",
                            "slug": "ser516asu-ser516-team-houston"
                        }
                    }
                ],
                "points": {
                    "9184536": 18295634
                },
                "total_points": 3.0
            },
            {
                "due_date": None,
                "due_date_reason": "",
                "due_date_status": "not_set",
                "assigned_to": None,
                "assigned_to_extra_info": None,
                "status": 9157381,
                "status_extra_info": {
                    "name": "New",
                    "color": "#70728F",
                    "is_closed": False
                },
                "project": 1521718,
                "project_extra_info": {
                    "name": "SER516-Team-Houston",
                    "slug": "ser516asu-ser516-team-houston",
                    "logo_small_url": None,
                    "id": 1521718
                },
                "id": 5468156,
                "ref": 10,
                "milestone": 376612,
                "is_closed": True,
                "created_date": "2024-01-29T21:10:13.537Z",
                "modified_date": "2024-02-14T14:04:42.010Z",
                "finish_date": "2024-02-12T06:11:07.431Z",
                "subject": "Get the data and compute the metric raw value.",
                "client_requirement": False,
                "team_requirement": False,
                "external_reference": None,
                "version": 3,
                "is_blocked": False,
                "blocked_note": "",
                "backlog_order": 1706562613537419,
                "sprint_order": 7,
                "kanban_order": 1706562613537422,
                "epics": [
                    {
                        "id": 218046,
                        "ref": 2,
                        "subject": "Cycle time",
                        "color": "#A3D350",
                        "project": {
                            "id": 1521718,
                            "name": "SER516-Team-Houston",
                            "slug": "ser516asu-ser516-team-houston"
                        }
                    }
                ],
                "points": {
                    "9184536": 18295635
                },
                "total_points": 5.0
            },
            {
                "due_date": None,
                "due_date_reason": "",
                "due_date_status": "not_set",
                "assigned_to": None,
                "assigned_to_extra_info": None,
                "status": 9157381,
                "status_extra_info": {
                    "name": "New",
                    "color": "#70728F",
                    "is_closed": False
                },
                "project": 1521718,
                "project_extra_info": {
                    "name": "SER516-Team-Houston",
                    "slug": "ser516asu-ser516-team-houston",
                    "logo_small_url": None,
                    "id": 1521718
                },
                "id": 5468157,
                "ref": 11,
                "milestone": 376612,
                "is_closed": False,
                "created_date": "2024-01-29T21:10:13.537Z",
                "modified_date": "2024-02-14T14:06:49.024Z",
                "finish_date": None,
                "subject": "Visualize the metric in an appropriate way.",
                "client_requirement": False,
                "team_requirement": False,
                "external_reference": None,
                "version": 2,
                "is_blocked": False,
                "blocked_note": "",
                "backlog_order": 1706562613537464,
                "sprint_order": 8,
                "kanban_order": 1706562613537466,
                "epics": [
                    {
                        "id": 218046,
                        "ref": 2,
                        "subject": "Cycle time",
                        "color": "#A3D350",
                        "project": {
                            "id": 1521718,
                            "name": "SER516-Team-Houston",
                            "slug": "ser516asu-ser516-team-houston"
                        }
                    }
                ],
                "points": {
                    "9184536": 18295635
                },
                "total_points": 5.0
            },
            {
                "due_date": None,
                "due_date_reason": "",
                "due_date_status": "not_set",
                "assigned_to": None,
                "assigned_to_extra_info": None,
                "status": 9157381,
                "status_extra_info": {
                    "name": "New",
                    "color": "#70728F",
                    "is_closed": False
                },
                "project": 1521718,
                "project_extra_info": {
                    "name": "SER516-Team-Houston",
                    "slug": "ser516asu-ser516-team-houston",
                    "logo_small_url": None,
                    "id": 1521718
                },
                "id": 5468200,
                "ref": 12,
                "milestone": 376612,
                "is_closed": False,
                "created_date": "2024-01-29T21:11:28.013Z",
                "modified_date": "2024-02-14T14:03:36.111Z",
                "finish_date": None,
                "subject": "Select a taiga project to apply it to.",
                "client_requirement": False,
                "team_requirement": False,
                "external_reference": None,
                "version": 2,
                "is_blocked": False,
                "blocked_note": "",
                "backlog_order": 1706562688013750,
                "sprint_order": 9,
                "kanban_order": 1706562688013755,
                "epics": [
                    {
                        "id": 218052,
                        "ref": 3,
                        "subject": "Lead Time",
                        "color": "#51CFD3",
                        "project": {
                            "id": 1521718,
                            "name": "SER516-Team-Houston",
                            "slug": "ser516asu-ser516-team-houston"
                        }
                    }
                ],
                "points": {
                    "9184536": 18295632
                },
                "total_points": 1.0
            },
            {
                "due_date": None,
                "due_date_reason": "",
                "due_date_status": "not_set",
                "assigned_to": None,
                "assigned_to_extra_info": None,
                "status": 9157381,
                "status_extra_info": {
                    "name": "New",
                    "color": "#70728F",
                    "is_closed": False
                },
                "project": 1521718,
                "project_extra_info": {
                    "name": "SER516-Team-Houston",
                    "slug": "ser516asu-ser516-team-houston",
                    "logo_small_url": None,
                    "id": 1521718
                },
                "id": 5468201,
                "ref": 13,
                "milestone": 376612,
                "is_closed": True,
                "created_date": "2024-01-29T21:11:28.013Z",
                "modified_date": "2024-02-14T14:02:45.347Z",
                "finish_date": "2024-02-12T06:12:39.072Z",
                "subject": "Configure the metric parameters.",
                "client_requirement": False,
                "team_requirement": False,
                "external_reference": None,
                "version": 2,
                "is_blocked": False,
                "blocked_note": "",
                "backlog_order": 1706562688013844,
                "sprint_order": 10,
                "kanban_order": 1706562688013847,
                "epics": [
                    {
                        "id": 218052,
                        "ref": 3,
                        "subject": "Lead Time",
                        "color": "#51CFD3",
                        "project": {
                            "id": 1521718,
                            "name": "SER516-Team-Houston",
                            "slug": "ser516asu-ser516-team-houston"
                        }
                    }
                ],
                "points": {
                    "9184536": 18295634
                },
                "total_points": 3.0
            },
            {
                "due_date": None,
                "due_date_reason": "",
                "due_date_status": "not_set",
                "assigned_to": None,
                "assigned_to_extra_info": None,
                "status": 9157381,
                "status_extra_info": {
                    "name": "New",
                    "color": "#70728F",
                    "is_closed": False
                },
                "project": 1521718,
                "project_extra_info": {
                    "name": "SER516-Team-Houston",
                    "slug": "ser516asu-ser516-team-houston",
                    "logo_small_url": None,
                    "id": 1521718
                },
                "id": 5468202,
                "ref": 14,
                "milestone": 376612,
                "is_closed": True,
                "created_date": "2024-01-29T21:11:28.013Z",
                "modified_date": "2024-02-14T14:02:27.532Z",
                "finish_date": "2024-02-12T06:28:47.024Z",
                "subject": "Get the data and compute the metric raw value.",
                "client_requirement": False,
                "team_requirement": False,
                "external_reference": None,
                "version": 2,
                "is_blocked": False,
                "blocked_note": "",
                "backlog_order": 1706562688013892,
                "sprint_order": 11,
                "kanban_order": 1706562688013895,
                "epics": [
                    {
                        "id": 218052,
                        "ref": 3,
                        "subject": "Lead Time",
                        "color": "#51CFD3",
                        "project": {
                            "id": 1521718,
                            "name": "SER516-Team-Houston",
                            "slug": "ser516asu-ser516-team-houston"
                        }
                    }
                ],
                "points": {
                    "9184536": 18295635
                },
                "total_points": 5.0
            },
            {
                "due_date": None,
                "due_date_reason": "",
                "due_date_status": "not_set",
                "assigned_to": None,
                "assigned_to_extra_info": None,
                "status": 9157381,
                "status_extra_info": {
                    "name": "New",
                    "color": "#70728F",
                    "is_closed": False
                },
                "project": 1521718,
                "project_extra_info": {
                    "name": "SER516-Team-Houston",
                    "slug": "ser516asu-ser516-team-houston",
                    "logo_small_url": None,
                    "id": 1521718
                },
                "id": 5468203,
                "ref": 15,
                "milestone": 376612,
                "is_closed": False,
                "created_date": "2024-01-29T21:11:28.013Z",
                "modified_date": "2024-02-14T14:02:06.566Z",
                "finish_date": None,
                "subject": "Visualize the metric in an appropriate way.",
                "client_requirement": False,
                "team_requirement": False,
                "external_reference": None,
                "version": 2,
                "is_blocked": False,
                "blocked_note": "",
                "backlog_order": 1706562688013938,
                "sprint_order": 12,
                "kanban_order": 1706562688013940,
                "epics": [
                    {
                        "id": 218052,
                        "ref": 3,
                        "subject": "Lead Time",
                        "color": "#51CFD3",
                        "project": {
                            "id": 1521718,
                            "name": "SER516-Team-Houston",
                            "slug": "ser516asu-ser516-team-houston"
                        }
                    }
                ],
                "points": {
                    "9184536": 18295635
                },
                "total_points": 5.0
            }
        ],
        "total_points": 48.0,
        "closed_points": 17.0
    }
        
      
    mock_get_milestone_by_id.return_value = mock_sprint_data

    with patch('requests.get') as mock_get:
       
      
        mock_get.return_value.json.return_value = mock_sprint_data


        result = get_storypoint_burndown_for_sprint(sprint_id, auth_token)

        assert result == expected_output







