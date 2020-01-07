from django.db import models
from markdownx.models import MarkdownxField
from markdownx.utils import markdownify

class Post(models.Model):
    """
    Model definition for ブログの投稿.    
    """
    title = models.CharField('タイトル', max_length=255)
    # content = models.TextField('本文')
    content = MarkdownxField('本文', help_text='write down in markdown format')
    
    created_at = models.DateTimeField('作成日', auto_now_add=True)
    updated_at = models.DateTimeField('更新日', auto_now=True)    


    class Meta:
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'

    def __str__(self):
        return self.title

    def formatted_markdown(self):
        return markdownify(self.content)