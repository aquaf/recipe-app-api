from celery import shared_task
from users.models import User


@shared_task
def hello():
    print("usercreated")