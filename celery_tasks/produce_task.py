# 生产者
from celery_tasks.task01 import send_email
from celery_tasks.task02 import send_msg

# delay实际上是在使用了cel.task装饰器
# 立即告知celery去执行task01  task02任务，并传入一个参数
result = send_email.delay("yuan")
# 异步任务return了一个ok，这个ok存放到了数据库中，不是赋值给了result
print(result.id)
result2 = send_email.delay("alex")
print(result2.id)
