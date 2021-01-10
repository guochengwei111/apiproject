import time
from celery_tasks.celery import cel


@cel.task
def send_msg(name):
    print("向%s发送邮件" % name)
    time.sleep(5)
    print("向%s发送邮件完成" % name)
    # retune的内容会到日志
    return "ok"
