# 异步的生产者
# 导入异步任务函数
from celery_tasks.yibu_celery import send_email
from datetime import datetime, timedelta

result = send_email.delay("yuan")
# 异步任务return了一个ok，这个ok存放到了数据库中，不是赋值给了result
print(result.id)
result2 = send_email.delay("alex")
print(result2.id)
# 当启动程序后，两个函数会同时执行，而不是result先执行完了再去执行result2
# 任何时刻消费者都会返回一个id值，可以随时调用id对应的数据

# 创建定时任务
# 方式一
# 设置任务启动时间
v1 = datetime(2021, 1, 11, 20, 50, 00)
# 时间转换成国标时间
v2 = datetime.utcfromtimestamp(v1.timestamp())
# 启动定时任务
result3 = send_email.apply_async(args=["egg"], eta=v2)
print(result3.id)

# 方式二
# 获取当前时间
ctime = datetime.now()
# 时间转换
utc_ctime = datetime.utcfromtimestamp(ctime.timestamp())
# 时间差为10秒
time_delay = timedelta(seconds=10)
# 当前时间 + 10秒
task_time = utc_ctime + time_delay
# 执行定时任务
result4 = send_email.apply_async(args=["egg"], eta=task_time)
print(result4)
