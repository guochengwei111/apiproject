from celery.result import AsyncResult
from celery_tasks.yibu_celery import cel

async_result = AsyncResult(id="", app=cel)

if async_result.successful():
    result = async_result.get()
    print(result)
    # result.forget()  #将结果删除
elif async_result.failed():
    print("执行失败")
elif async_result.status == "PENDING":
    print("任务等待中被执行")
elif async_result.status == "RETRY":
    print("任务异常后正在重试")
elif async_result.status == "STARTED":
    print("任务异常后正在重试")
