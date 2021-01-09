"""
关联模型的序列化，分页，过滤，认证，权限和限流
将rest_framework注册到项目中

Python类型数据序列化(serialization)
每种编程语言都有各自的数据类型,
将属于自己语言的数据类型或对象转换为可通过网络传输或可以存储到本地磁盘的数据格式
（如：XML、JSON或特定格式的字节串）的过程称为序列化(seralization)；反之则称为反序列化。
API开发的本质就是各种后端语言的自己的数据类型序列化为通用的可读可传输的数据格式，比如常见的JSON类型数据。
"""
import json

print(json.dumps({"name": "John", "score": 99}))

from django.core import serializers

# print(serializers.serialize("json", SomeModel.objdec.all()))
# data1 = serializers.serialize("json", SomeModel.objects.all(), fields=('name','id'))
# data2 = serializers.serialize("json", SomeModel.objects.filter(field = some_value))

# ValuesQuerySet对象不能用 serializers.serialize() 方法序列化成json,
# 需要先转换成list再用 json.dumps()方法序列化成json格式

"""
from django.core.serializers.json import DjangoJSONEncoder
queryset = myModel.objects.filter(foo_icontains=bar).values('f1', 'f2', 'f3')
data4 = json.dumps(list(queryset), cls=DjangoJSONEncoder)
"""

"""
什么是符合RESTful规范的API?
REST是REpresentational State Transfer三个单词的缩写，
由Roy Fielding于2000年论文中提出。简单来说，就是用URI表示资源，
用HTTP方法(GET, POST, PUT, DELETE)表征对这些资源进行操作。而如果想你的api被称为restful api，只要遵循其规定的约束

协议、域名和版本
uri(统一资源标识符)  //用名词复数，因为数据库中表都是同种记录的集合
---------------------------------------------------------------------------------------
一个 URI就应该是一个资源，本身不能包含任何动作。REST的规范是资源的URI地址是固定不变的，
对同一资源应使用不同的HTTP请求方法进行不同的操作，比如常见的增删查改。

[POST]    https://api.example.com/v1/users   // 新增
[GET]     https://api.example.com/v1/users/1 // 查询
[PATCH]   https://api.example.com/v1/users/1 // 更新
[PUT]     https://api.example.com/v1/users/1 // 覆盖，全部更新
[DELETE]  https://api.example.com/v1/users/1 // 删除

url中使用- 而不是_  每个url结尾不能加斜线/

-----------------------------------------------------------------------------------------
HTTP请求方法
GET（SELECT）：从服务器取出资源（一项或多项）。
POST（CREATE）：在服务器新建一个资源。
PUT（UPDATE）：在服务器更新资源（客户端提供改变后的完整资源）。
PATCH（UPDATE）：在服务器更新资源（客户端提供改变的属性）。
DELETE（DELETE）：从服务器删除资源。

---------------------------------------------------------------------------------------------
过滤信息（Filtering）

?limit=10：指定返回记录的数量
?offset=10：指定返回记录的开始位置。
?page=2&per_page=100：指定第几页，以及每页的记录数。
?sortby=name&order=asc：指定返回结果按照哪个姓名排序，以及排序顺序。
?user_type_id=1：指定筛选条件，比如用户类型

---------------------------------------------------------------------------------------------
状态码（Status Codes）

200 OK - [GET]：服务器成功返回用户请求的数据，该操作是幂等的（Idempotent）。
201 CREATED - [POST/PUT/PATCH]：用户新建或修改数据成功。
202 Accepted - [*]：表示一个请求已经进入后台排队（异步任务）
204 NO CONTENT - [DELETE]：用户删除数据成功。
400 INVALID REQUEST - [POST/PUT/PATCH]：用户发出的请求有错误，服务器没有进行新建或修改数据的操作，该操作是幂等的。
401 Unauthorized - [*]：表示用户没有权限（令牌、用户名、密码错误）。
403 Forbidden - [*] 表示用户得到授权（与401错误相对），但是访问是被禁止的。
404 NOT FOUND - [*]：用户发出的请求针对的是不存在的记录，服务器没有进行操作，该操作是幂等的。
406 Not Acceptable - [GET]：用户请求的格式不可得（比如用户请求JSON格式，但是只有XML格式）。
410 Gone -[GET]：用户请求的资源被永久删除，且不会再得到的。
422 Unprocesable entity - [POST/PUT/PATCH] 当创建一个对象时，发生一个验证错误。
500 INTERNAL SERVER ERROR - [*]：服务器发生错误

------------------------------------------------------------------------------------------------------------
Hypermedia API
RESTful API最好做到Hypermedia，即返回结果中提供链接，连向其他API方法，使得用户不查文档，也知道下一步应该做什么。
比如，当用户向api.example.com的根目录发出请求，会得到这样一个文档。

{"link": {
  "rel":   "collection https://www.example.com/zoos",
  "href":  "https://api.example.com/zoos",
  "title": "List of zoos",
  "type":  "application/vnd.yourformat+json"
}}
"""
