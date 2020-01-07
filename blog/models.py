from django.db import models
from markdownx.models import MarkdownxField
from markdownx.utils import markdownify



class Tag(models.Model):
    """ 記事につけるタグクラス　"""
    name = models.CharField('タグ名', max_length=255)
    slug = models.SlugField('タグスラグ', unique=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Post(models.Model):
    """
    Model definition for ブログの投稿.    
    """
    title = models.CharField('タイトル', max_length=255)
    description = models.CharField('説明', max_length=255, blank=True, default='', null=True)
    content = MarkdownxField('本文', help_text='write down in markdown format')
    
    tags = models.ManyToManyField(Tag, blank=True)

    created_at = models.DateTimeField('作成日', auto_now_add=True)
    updated_at = models.DateTimeField('更新日', auto_now=True)    


    class Meta:
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'

    def __str__(self):
        return self.title

    def formatted_markdown(self):
        return markdownify(self.content)