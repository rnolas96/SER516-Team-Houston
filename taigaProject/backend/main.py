from fastapi import FastAPI
from controller.userstory_controller import userstory_router
from controller.task_controller import task_router
from controller.login_controller import login_router
from controller.project_controller import project_router

from taigaApi.issue.getCustomAttributeValueByIssueId import get_custom_attribute_value_by_issue_id

app = FastAPI()
app.include_router(userstory_router, prefix='/api/userstory')
app.include_router(task_router, prefix='/api/task')
app.include_router(login_router, prefix='/api')
app.include_router(project_router, prefix='/api/project')




project_id = 1525740
auth_token = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzA5MzM4MzE0LCJqdGkiOiI4NDAyZTZkOGNmNWQ0NzM1YWU3YWQ2YjczYTc5NDJjNyIsInVzZXJfaWQiOjYxODc2MX0.iGNzXaAbFg61oL6QK77Nv4Rny0kHOvd07b0xI7CguoGFYUi3HxOSA_MBQd7eb3VhgS7PT_lY13cb9-mAkfnHrcDX5EhPBs0kKVUGOwRC_hxtljPjcACfyQTTMr7x_qFp_diPC0l09-1M3v-lmAF19fwoHbJQr692GOZbiq_zU2LwGhIp6NkCCL7oBrZjp5TVoUU8T6a74P1qQa1H_qL5_16HZTLXSckDmBtOdbc1FICbBKVUELc69X7ox82LkXhRL2QfqZ32kGjKRFYKMPc6ZXIhe4oGZYfYeYdzGiNP2aLxStS4KMaAi13nepFE721-v7PF92DckiCKWyou0ARMrg"
issue_id = 1729278
attribute_id = '18181'
print("result=======", get_custom_attribute_value_by_issue_id(issue_id, attribute_id, auth_token))