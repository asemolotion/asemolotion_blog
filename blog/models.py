import os
import re
import boto3
from django.conf import settings
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


class FileLink(models.Model):

	filepath = models.CharField('ファイルパス', max_length=255)  #  url max is 2048 chars
	post = models.ForeignKey('Post', on_delete=models.CASCADE)
	# 参照しているPostデータが消えたらFileLinkは全て消すのでCASCADEでいい。

	def __str__(self):
		return self.filepath

class Post(models.Model):
	"""
	Model definition for ブログの投稿.    
	"""
	title = models.CharField('タイトル', max_length=255)
	description = models.CharField('説明', max_length=255, blank=True, default='', null=True)
	content = MarkdownxField('本文', help_text='write down in markdown format')
	
	tags = models.ManyToManyField(Tag, blank=True)
	project = models.ForeignKey(Project, on_delete=models.PROTECT, null=True, blank=True, default=None)

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


	created_at = models.DateTimeField('作成日', auto_now_add=True)
	updated_at = models.DateTimeField('更新日', auto_now=True)    

	class Meta:
		verbose_name = 'Post'
		verbose_name_plural = 'Posts'

	def __str__(self):
		return self.title

	def formatted_markdown(self):
		return markdownify(self.content)

	
	def save(self, **kwargs):

		# print(self.content)
		
		self.check_filelink_diffs()

		super().save(**kwargs)

	def check_filelink_diffs(self):

		# もともとあったfilepathを取り出して集合にする
		old_filelinks_queryset = self.filelink_set.values_list('filepath', flat=True)
		old_filelinks = set(list(old_filelinks_queryset))

		# ![](linkurl)という画像のマークアップを全て取り出す
		img_ptns = re.findall(
			r'!\[\].*\.png',
			self.content
		)

		# 画像マークアップからファイルパスを全て取り出す
		filelinks = []
		for ptn in img_ptns:
			filelink = re.search(r'/\w+/\w+/.*\.png', ptn).group()  # search()は最初の一個のみ。
			filelinks.append(filelink)

		# filelinksになくて、old_filelinksにあるものを消す
		filelinks_diff = list(old_filelinks - set(filelinks))
		
		for diff in filelinks_diff:
			# FileLinkデータを消す
			FileLink.objects.filter(
				filepath=diff
			).delete()

			print('消すもの: ', diff)
			# ファイルの実体を消す
			if settings.DEBUG:				
				delete_filepath = os.path.abspath(os.path.join(settings.BASE_DIR, diff[1:]))  # diff もslashスタートなので、ルートと思ってjoinできない。
				print('ファイルパスは: ', delete_filepath)
				os.remove(delete_filepath)
			
			else:
				# s3で
				s3 = boto3.resource('s3')
				bucket = s3.Bucket('asemolotion-blog')
				bucket.delete_object(diff)
				

		# 今あるものはそのまま、追加分は追加の update_or_create()
		for filelink in filelinks:
			FileLink.objects.update_or_create(
				filepath = filelink,
				post = self
			)
		
		
		

