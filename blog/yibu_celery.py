# celery
"""
基于生产者，消费者模型
主要应用场景：异步任务和定时任务
"""
# 生产者---消息队列（消息中间件）---消费者---结果存储
import celery
import time

backend = "redis://127.0.0.1:6379/1"  # 异步任务存储库
broker = "redis://127.0.0.1:6379/2"  # 消息中间件
#                   和项目相关的名字
cel = celery.Celery("test", backend=backend, broker=broker)


@cel.task
def send_email(name):
    print("向%s发送邮件" % name)
    time.sleep(5)
    print("向%s发送邮件完成" % name)
    return "ok"


@cel.task
def send_mesg(name):
    print("向%s发送短信" % name)
    time.sleep(5)
    print("向%s发送短信完成" % name)
    return "ok"

# 执行任务的命令
#                  程序名          日志
# celery worker -A yibu_celery -l info
# 在终端执行上面的命令后，会扫描消费者，就是监听异步任务，这时候任务还没有启动
# 任务的启动由生产者决定，生产者发出的消息队列会被消费者异步任务监听到后执行
