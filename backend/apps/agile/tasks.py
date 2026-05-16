from celery import shared_task
from django.utils import timezone
from apps.agile.models import Task

@shared_task
def send_task_created_notification(task_id):
    print (f"Task created with ID: {task_id}. Sending notification...")
    return f"Notification sent for task ID: {task_id}"

@shared_task
def check_overdue_tasks():
    today = timezone.localdate()

    overdue_tasks = Task.objects.filter(
        due_date__lt=today,
    ).exclude(status="done")

    count = overdue_tasks.count()

    print(f"Found {count} overdue tasks")
    return f"Found {count} overdue tasks"

