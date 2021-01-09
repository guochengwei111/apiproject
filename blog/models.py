from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import get_user_model

# Create your models here.

User = get_user_model()


class Article(models.Model):
    """Article Model"""
    # # 惰性翻译 gettext_lazy() 被调用时翻译
    STATUS_CHOICES = (
        ("p", _("Published")),  # 发表
        ("d", _("Draft"))  # 草稿
    )
    title = models.CharField(verbose_name=_("Title(*)"), max_length=90, db_index=True)
    body = models.TextField(verbose_name=_("Body"), blank=True)
    author = models.ForeignKey(to=User, verbose_name=_("Author"), on_delete=models.CASCADE, related_name="articles")
    status = models.CharField(_("Status(*)"), max_length=1, choices=STATUS_CHOICES, default="s", null=True, blank=True)
    create_date = models.DateTimeField(verbose_name=_("Create Date"), auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["-create_date"]
        verbose_name = "Article"
        verbose_name_plural = "Articles"

    from django.template.defaultfilters import slugify
"""
slug是一个报纸术语，slug是一个种短标签，只包含字母，数字，下划线或连字符。通常用于url中，有利于seo
slug是一种生成有效url的方法，通常用在已经获得的数据。例如：使用文章标题生成URL。
像这种建议是用函数给定标题或者其他数据生成slug，而不是手动设置。

class Article(models.Model):
    title = models.CharField(max_length=100)

    def slug(self):
        return slugify(self.title)
"""

