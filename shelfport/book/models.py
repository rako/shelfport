from accounts.models import CustomUser
from django.db import models

# Create your models here.
class Book(models.Model):
    user = models.ForeignKey(CustomUser, verbose_name='ユーザー', on_delete=models.PROTECT)
    title = models.CharField(verbose_name='書籍名', max_length=255)
    isbn = models.CharField(verbose_name='ISBN', max_length=13) # ISBNは13桁で必須にしておきリストで管理するときのプライマリキーにする
    content = models.TextField(verbose_name='書籍概要', blank=True, null=True)
    image = models.ImageField(verbose_name='表紙画像', blank=True, null=True)
    refer = models.TextField(verbose_name='引用', blank=True, null=True)
    refer_url = models.URLField(verbose_name='参考URL', blank=True, null=True)
    created_at = models.DateTimeField(verbose_name='登録日', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='更新日', auto_now=True)

    class Meta:
        verbose_name_plural = '書籍'
    
    def __str__(self):
        return self.title