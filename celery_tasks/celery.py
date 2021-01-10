# 多任务异步
# 不同的异步任务要单独放在一个模块里面，如task01  task02
# 配置celery
from datetime import timedelta

from celery import Celery
from celery.schedules import crontab

cel = Celery(
    "celery_demo",  # 异步对应的应用名称
    broker="127.0.0.1:6379/1",  # 存放消息队列
    backend="127.0.0.1:6379/2",  # 存放异步任务结果
    include=["celery_tasks.task01", "celery_tasks.task02"]  # 对应的异步任务
)
# 时区配置
cel.conf.timezone = "Asia/Shanghai"
# 是否使用UTC
cel.conf.enable_utc = False

# cd到当前文件目录然后执行启动命令
#                  执行的异步文件    日志    并发用协程
# celery borker -A celery_tasks -l info -P eventlet
# 回车之后会有日志  提示异步任务监听成功

# 定时任务的配置
# 需要承接上面的配置
# 定时任务不需要再创建生产者了，由定时任务直接往消息队列添加任务
# 需要注意的是，需要先启动消费者监听队列，再启动往队列添加消息，是两天命令都在终端执行
# celery -A celery_tasks worker -l info # 监听消息队列 如果启动之后直接有任务运行，那说明是系统之前就放在队列中的历史没有执行完
# celery -A celery_tasks worker -l info -c 5 # 同时启动5个并发任务执行遗留队列
# 如果上面启动没有遗留任务会显示ready 接着用下面的命令启动启动定时任务
# celery beat -A celery_tasks   # beat 之后会启动celery配置，配置里面有定时向队列添加消息
# Local 有两个 需要分别关闭worker  和 beat  ctrl+c分别关闭两个
# import redis
# r= redis.Redis(host="",port="",db=1)
# r.delete("celery")    # 删除某个键
# for i in r.lrange("celery键名", 0, -1): # 把celery键名遍历
#     print(i)
cel.conf.beat_schedule = {
    # 任意起一个任务名字，最好见名知意
    # 每十秒向消息队列添加一个任务
    "add-every-10-seconds": {
        "task": "celery_tasks.task01_send_email",
        "schedule": 10,  # 每10秒添加一个任务
        # "schedule": crontab(minute="*/1"),  # 每1分钟添加一个任务
        # "schedule": timedelta(seconds=10)  # 每10秒添加一个任务,这个参数会设置更灵活
        "args": ["张三"]  # 如果任务需要传参就设置这个参数
    }
}
