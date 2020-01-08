from django.db import models
from markdownx.models import MarkdownxField
from markdownx.utils import markdownify

class Project(models.Model):
	""" Postが所属するプロジェクト　"""
	name = models.CharField('プロジェクト名', max_length=255)
	slug = models.SlugField('プロジェクトスラグ', unique=True)
	timestamp = models.DateTimeField(auto_now_add=True)
	
	class Meta:
		verbose_name = 'Project'
		verbose_name_plural = 'Projects'

	def __str__(self):
		return self.name


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

	STATUS = (
		('draft', '下書き'),
		('released', '公開'),
	)
	status = models.CharField('状態', max_length=50, choices=STATUS, default='draft')
	
	RELEASE_CONDITION = (
		('public', '全員に公開'),
		('limited', 'LIMITED')
	)
	release_condition = models.CharField('閲覧制限', max_length=50, choices=RELEASE_CONDITION, default='limited')
	
	POST_TYPE = (
		('article', 'Article'),
		('short_code', 'ShortCode')
	)
	post_type = models.CharField('タイプ', max_length=50, choices=POST_TYPE, default='article')

	project = models.ForeignKey(Project, on_delete=models.PROTECT, null=True, blank=True, default=None)


	created_at = models.DateTimeField('作成日', auto_now_add=True)
	updated_at = models.DateTimeField('更新日', auto_now=True)    


	class Meta:
		verbose_name = 'Post'
		verbose_name_plural = 'Posts'

	def __str__(self):
		return self.title

	def formatted_markdown(self):
		return markdownify(self.content)