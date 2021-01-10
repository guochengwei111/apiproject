# celery的配置文件
# 注意文件都是包  里面时有init.py的
# 可以再mycelry下面创建不同的任务模块，模块里面都只能有tasks.py，不能使用别的名字
broker_url = "redis://127.0.0.1:6379/15"
result_backend = "redis://127.0.0.1:6379/14"
