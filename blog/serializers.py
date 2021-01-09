# 序列化器
from rest_framework import serializers
from blog.models import Article
from django.contrib.auth import get_user_model

User = get_user_model()


class ArticleSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(required=True, allow_blank=True, max_length=90)
    body = serializers.CharField(required=True, allow_blank=True)
    author = serializers.ReadOnlyField(source="author.id")
    status = serializers.ChoiceField(choices=Article.STATUS_CHOICES, default="p")
    create_date = serializers.DateTimeField(read_only=True)

    def create(self, validated_data):
        """
        Create a new "article" instance
        :param validated_data:
        :return:
        """
        return Article.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Use validated data to return an existing `Article`instance
        使用已验证的数据返回现有的“Article”实例
        :param instance:模型对象
        :param validated_data: 反序列化后的字典数据
        :return:
        """
        instance.title = validated_data.get("title", instance.title)
        instance.body = validated_data.get("body", instance.body)
        instance.status = validated_data.get("status", instance.status)
        instance.save()
        return instance


"""  
# 序列化器类的第一部分定义了序列化/反序列化的字段。create()和update()方法定义了在调用serializer.save()时如何创建和修改完整的实例。
# 
# 序列化器类与Django Form类非常相似，并在各种字段中设置各种验证，例如required，max_length和default。
# 
# 注意：定义序列化器时一定要注明哪些是仅可读字段(read-only fields)，哪些是普通字段。对于read-only fields，客户端是不需要也不能够通过POST或PUT请求提交相关数据进行反序列化的。
# 
# 本例中ID和create_date都是由模型自动生成，每个article的author我们也希望在视图中与request.user绑定，而不是由用户通过POST或PUT自行修改，所以这些字段都是read-only。相反title，body和status是用户可以添加或修改的字段，所以不能设成read-only。
"""

"""
B站序列化教程笔记
序列化：将模型转换成json
# 序列化器的类应该单独创建一个serializers.py
1.定义序列化器类（模型名或者类视图名+Serializer）继承Serializer
2.定义序列化器中的字段 参照模型（序列化器中的字段可以比模型多或少 如果表示是模型中的字段在序列器中这个字段名应该和模型中的字段名一致）
3.如果在多里面关联序列化一（外键名）   如果是在一里面关联序列化多（多的一方模型名小写_set）
4.如果在一的一方关联序列化多时，还需要指定关联字段（many=True）
5.将要序列化的模型或查询集传给序列化器类的instance参数 如果传的时查寻集 多指定many=True（多指的是列表不是单个数据）
6.获取序列化后的数据 序列化器对象名.data属性
序列化就是一个单纯的模型转字典

反序列化：json转模型
拿到前端传入的数据-》序列化器的data->调用序列化器的.is_valid()方法进行校验-》调用序列化器的.save()方法
1.获取前端传入的json字典数据
2.创建序列化器给序列化器的data参数用关键字传参
3.调用序列化器的.is_valid(raise_execption=True)进行校验，如果校验出错会自动抛出错误信息
4.调用序列化器的.save()方法，调用save时会判断当初创建序列化器时是否传入instance
5.如果传入了instance 也传了打他，那么调用save实际调用序列化器中的update方法，反之就时调用序列化器中的create方法
6.反序列化最后会自动帮你完成序列化，return到前端的时serializer.data数据
"""


# 我们的ArticleSerializer类中重复了很多包含在Article模型（model）中的字段信息。
# 使用ModelSerializer类可以重构我们的序列化器类，使整体代码更简洁。
#
# 再次打开blog/serializers.py文件，并将ArticleSerializer类替换为以下内容。两者作用是一样的。

class ArticleModelSerializer(serializers.ModelSerializer):
    # password = serializers.CharField(max_length=20)   # 还可以添加自定义映射字段

    class Meta:
        model = Article
        fields = "__all__"
        # fields = ["id", "author"]   # 只映射列表中的指定字段
        # exclude = ["create_date"]   # 排除列表中的字段，只映射列表之外的字段

        # 如果要修改某个字段中的选项参数
        extra_kwargs = {
            "字段名1": {"属性名": "属性值", "required": True},
            "字段名2": {"min_value": 0, "write_only": True},  # 只写时反序列化时使用  字典转模型
        }
        # 设置字段只读 序列化操作  模型转json
        read_only_fields = ("id", "author", "create_date")
