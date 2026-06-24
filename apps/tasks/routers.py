# apps/tasks/routers.py

from fastapi import APIRouter
from celery.result import AsyncResult

from apps.tasks.schemas import EmailRequest, EmailResponse
from apps.tasks.email import send_email
from celery_utils import celery_app

tasks_router = APIRouter(tags=['tasks'])


@tasks_router.post(
    "/send-email",
    response_model=EmailResponse
)
async def send_email_endpoint(
    request: EmailRequest
):
    task = send_email.delay(request.email)

    return EmailResponse(
        message="Email sending task created",
        task_id=task.id,
    )


@tasks_router.get("/tasks/{task_id}")
async def get_task_status(task_id: str):
    task_result = AsyncResult(
        task_id,
        app=celery_app
    )

    return {
        "task_id": task_id,
        "status": task_result.status,
        "result": task_result.result if task_result.ready() else None,
    }



# from fastapi import APIRouter
#
# from apps.tasks.email import send_email
# from apps.tasks.schemas import EmailRequest, EmailResponse
#
# tasks_router = APIRouter(tags=['tasks'])
#
#
# @tasks_router.post('/send-email', response_model=EmailResponse)
# def send_email_endpoint(payload: EmailRequest):
#     task = send_email.delay(payload.email)
#     return EmailResponse(task_id=task.id)