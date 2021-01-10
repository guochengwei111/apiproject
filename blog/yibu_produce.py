# 异步的生产者
# 导入异步任务函数
from blog.yibu_celery import send_email, send_mesg

result = send_email.delay("yuan")
# 异步任务return了一个ok，这个ok存放到了数据库中，不是赋值给了result
print(result.id)
result2 = send_email.delay("alex")
print(result2.id)
# 当启动程序后，两个函数会同时执行，而不是result先执行完了再去执行result2
# 任何时刻消费者都会返回一个id值，可以随时调用id对应的数据
