import time
from celery_tasks.celery import cel


@cel.task
def send_email(name):
    print("向%s发送邮件" % name)
    time.sleep(5)
    print("向%s发送邮件完成" % name)
    return "ok"
