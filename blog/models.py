from django.db import models

# Create your models here.

class Post(models.Model):
    """
    Model definition for ブログの投稿.    
    """
    title = models.CharField('タイトル', max_length=255)
    content = models.TextField('本文')
    
    created_at = models.DateTimeField('作成日', auto_now_add=True)
    updated_at = models.DateTimeField('更新日', auto_now=True)    


    class Meta:
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'

    def __str__(self):
        return self.title
