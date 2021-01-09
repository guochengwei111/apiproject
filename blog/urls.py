from django.urls import re_path
from rest_framework.urlpatterns import format_suffix_patterns
from blog import views

from rest_framework.routers import DefaultRouter  # 默认路由器

urlpatterns = [
    # re_path(r"^articles/$", views.article_list),
    # re_path(r"^articles/(?P<pk>[0-9]+)$", views.article_detail),
    # APIView
    # re_path(r"^articles/$", views.ArticleListAPIView.as_view()),
    # re_path(r"^articles/(?P<pk>[0-9]+)$", views.ArticleDetailAPIView.as_view())
    # APIView
    re_path(r"^articles/$", views.ArticleListGenericView.as_view()),
    re_path(r"^articles/(?P<pk>[0-9]+)$", views.ArticleDetailGenericView.as_view())
]

urlpatterns = format_suffix_patterns(urlpatterns=urlpatterns)

# ----------------------------类似上面的功能----------------------------------
router = DefaultRouter()  # 创建路由器对象
router.register(r"books前缀，如上面的articles", views.BookInfoView)  # 注册路由
urlpatterns += router.urls  # 把注册好的路由拼接到urlpatterns
# ------------------------------------------------------------

# http://127.0.0.1:8000/v1/articles
# 注意：DRF默认是以可浏览的api形式展示返回响应结果的(articles.api)，
# 如果你只需要返回最简单的json格式的数据，只需要在访问地址后面加上.json后缀即可(articles.json)
# http://127.0.0.1:8000/v1/articles.json

"""
# 在POST的时候注意格式，最后一行数据后面不要有逗号否则，多了一个逗号报错
# "detail": "JSON parse error - Expecting value: line 1 column 5 (char 4)"
{
    "title": "ni hao b",
    "body": "你好啊啊啊啊",
    "status": "p"
}
"""
