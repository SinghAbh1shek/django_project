from celery import shared_task
from time import sleep


@shared_task
def test_task(x, y):
    sleep(5)
    return f"x: {x}, y: {y}"