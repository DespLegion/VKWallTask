from celery import shared_task
from .utils import upload_cover


@shared_task(name="Update cover task")
def update_cover_task():
    task_res = upload_cover()
    return task_res
