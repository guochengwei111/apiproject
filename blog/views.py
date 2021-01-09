from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from blog.models import Article
from blog.serializers import ArticleSerializer

from rest_framework.viewsets import ModelViewSet


# Create your views here.

@api_view(["GET", "POST"])
def article_list(request, format=None):
    """
    List all articles,or create a new article.
    :param request:
    :return:
    """
    if request.method == "GET":
        articles = Article.objects.all()
        # many=True 如果序列化的对象是一个数据集就需要这个参数
        # 如果查询的是一个单一的数据，比如article = Article.objects.get(pk=pk) 就不需要这个参数
        serializer = ArticleSerializer(articles, many=True)
        return Response(serializer.data)
    elif request.method == "POST":
        serializer = ArticleSerializer(data=request.data)
        if serializer.is_valid():
            # 注意：由于序列化器中author是read-only字段，用户是无法通过POST提交来修改的，
            # 我们在创建Article实例时需手动将author和request.user绑定，如下所示：
            serializer.save(author=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "PUT", "DELETE"])
def article_detail(request, pk, format=None):
    """
    Retrieve(检索),update or delete an article instance.
    :param request:
    :param pk:
    :return:
    """
    try:
        article = Article.objects.get(pk=pk)
    except Article.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == "GET":
        serializer = ArticleSerializer(article)
        return Response(serializer.data)
    elif request.method == "PUT":
        serializer = ArticleSerializer(article, data=request.data)
        # raise_exception=True自动抛出异常信息
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == "DELETE":
        article.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


"""
这里我们使用了DRF提供的@api_view这个非常重要的装饰器，实现了以下几大功能：

与Django传统函数视图相区分，强调这是API视图，并限定了可以接受的请求方法。
拓展了django原来的request对象。新的request对象不仅仅支持request.POST提交的数据，
还支持其它请求方式如PUT或PATCH等方式提交的数据，所有的数据都在request.data字典里。这对开发Web API非常有用。

request.POST  # 只处理表单数据  只适用于'POST'方法
request.data  # 处理任意数据  适用于'POST'，'PUT'和'PATCH'方法
"""


# B站教程
class BookInfoView(ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer


from rest_framework.response import Response
from blog.serializers import ArticleModelSerializer
from rest_framework import status

from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView  # 通用视图 继承上面的APIView
from rest_framework.mixins import ListModelMixin, CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, \
    DestroyModelMixin
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView, RetrieveDestroyAPIView
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView


class ArticleListAPIView(APIView):
    # 列表视图  跟上面的函数视图一样，只不过做了method的判断而已
    def get(self, request):
        # 查询所有数据集
        all_articles = Article.objects.all()
        # 对数据集进行序列化 数据集为多时用many=True
        serializer = ArticleModelSerializer(instance=all_articles, many=True)
        # 返回前端响应
        return Response(serializer.data)

    def post(self, request):
        # 新增
        # 1.获取前端传入的请求体数据
        data = request.data
        # 2.创建序列化器进行反序列化
        serializer = ArticleModelSerializer(data=data)
        # 3.电泳序列化器的.is_valid方法进行校验，并自动抛出异常信息
        serializer.is_valid(raise_exception=True)
        # 4.调用序列化器的save方法进行执行create方法
        serializer.save(author=request.user)
        # 5.响应
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ArticleDetailAPIView(APIView):
    # 列表视图  跟上面的函数视图一样，只不过做了method的判断而已
    def get(self, request, pk):
        # 查询单个数据集
        try:
            article = Article.objects.get(pk=pk)
        except Article.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        # 对数据集进行序列化 数据集为多时用many=True 单个数据集不需要这个参数
        serializer = ArticleModelSerializer(instance=article)
        # 返回前端响应
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        # 修改数据
        # 1.查询pk对应的单个数据
        try:
            article = Article.objects.get(pk=pk)
        except Article.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        # 获取前端传过来的数据
        data = request.data
        # 2.创建序列化器
        serializer = ArticleModelSerializer(instance=article, data=data)
        # 3.校验  不需要if判断 有异常直接抛出
        serializer.is_valid(raise_exception=True)
        # 4.save
        serializer.save(author=request.user)
        # 5.响应
        return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)

    def detele(self, request, pk):
        # 删除
        # 1.查询pk对应的单个数据
        try:
            article = Article.objects.get(pk=pk)
        except Article.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        # 2.如果找到对应的数据，直接删除操作
        article.delete()
        # 3.返回响应
        return Response(status=status.HTTP_204_NO_CONTENT)


# 通用类视图 和上面的功能时一样的，只不过序列器和数据集都是可变的了
class ArticleListGenericView(GenericAPIView, ListModelMixin, CreateModelMixin):
    # 指定序列化器类
    serializer_class = ArticleModelSerializer
    # 指定查寻集”数据来源“
    queryset = Article.objects.all()

    def get(self, request):
        # all_articles = self.get_queryset()
        # serializer = self.get_serializer(all_articles, many=True)
        # return Response(serializer.data)
        # self.list()调用的是ListModelMixin，该方法封装了上面三行代码的功能
        return self.list(request)

    def post(self, request):
        # 获取前端传过来的数据并创建序列化器
        # serializer = self.get_serializer(data=request.data)
        # # 校验
        # serializer.is_valid(raise_exception=True)
        # # 保存
        # serializer.save()
        # # 响应
        # return Response(serializer.data, status=status.HTTP_201_CREATED)
        # 主要使用了CreateModelMixin扩展
        return self.create(request=request)


class ArticleDetailGenericView(GenericAPIView, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin):
    # get put delete中注释掉的内容，是没有使用mixin扩展的
    # 指定序列化器类
    serializer_class = ArticleModelSerializer
    # 指定查寻集”数据来源“
    queryset = Article.objects.all()

    def get(self, request, pk):
        # # 源码里面用到了pk
        # article = self.get_object()
        # # 创建序列化对象
        # serializer = self.get_serializer(article)
        # # 响应对象的.data属性
        # return Response(serializer.data)
        return self.retrieve(request, pk)

    def put(self, request, pk):
        # # 先查找对应的模型，因为是修改更新操作
        # article = self.get_object()
        # # 创建序列化器对象                  对应模型   前端传来的数据
        # serializer = self.get_serializer(article, request.data)
        # # 校验数据
        # serializer.is_valid(raise_exception=True)
        # # 保存数据
        # serializer.save()
        # # 响应数据
        # return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)
        return self.update(request, pk)

    def delete(self, request, pk):
        # # 先查找对应的数据模型
        # article = self.get_object()
        # # 删除
        # article.delete()
        # # 响应
        # return Response(status=status.HTTP_204_NO_CONTENT)
        return self.destroy(request, pk)


from rest_framework.viewsets import ViewSet


# 视图集
# 五个数据库操作写在一个类视图里面，重写了as_view()

class ArticleViewSet(ViewSet):
    # 查询所有
    def list(self, request):
        # 获取数据列表
        articles = Article.objects.all()
        # 创建序列化器
        serializer = ArticleModelSerializer(instance=articles, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # 查询单一
    def retrieve(self, request, pk):
        # 查询模型数据
        try:
            article = Article.objects.get(pk=pk)
        except article.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        # 创建序列化器
        serializer = ArticleModelSerializer(article)
        # 响应数据
        return Response(serializer.data, status=status.HTTP_200_OK)

    # 创建模型数据
    def create(self, request):
        # 创建序列化器
        serializer = ArticleModelSerializer(data=request.data)
        # 验证数据
        serializer.is_valid(raise_exception=True)
        # 保存数据
        serializer.save()
        # 响应数据
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    # 修改模型数据
    def update(self, request, pk):
        # 查询数据库对象
        try:
            article = Article.objects.get(pk=pk)
        except article.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        # 创建序列化器
        serializer = ArticleModelSerializer(instance=article, data=request.data)
        # 校验数据
        serializer.is_valid(raise_exception=True)
        # 保存数据
        serializer.save()
        # 响应数据
        return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)

    # 删除数据
    def destroy(self, request, pk):
        try:
            article = Article.objects.get(pk=pk)
        except article.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        article.delete()
        # 响应
        return Response(status=status.HTTP_204_NO_CONTENT)
