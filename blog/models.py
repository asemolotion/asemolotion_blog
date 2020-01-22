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
	
	RELEASE_CONDITION = (
		('public', '全員に公開'),
		('limited', 'LIMITED')
	)
	release_condition = models.CharField('閲覧制限', max_length=50, choices=RELEASE_CONDITION, default='limited')
		
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

	def delete(self):
		if settings.DEBUG:  # ローカルの時
			delete_filepath = os.path.abspath(os.path.join(settings.BASE_DIR, self.filepath[1:]))  # diff もslashスタートなので、ルートと思ってjoinできない。
			print('ファイルパスは: ', delete_filepath)
			os.remove(delete_filepath)
		
		else:
			# s3のファイルを消す時
			try:
				# ローカルプロダクションの時は環境変数から取れないので、読み込む
				from conf.local_settings import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY
				session = boto3.Session(
					aws_access_key_id=AWS_ACCESS_KEY_ID,
					aws_secret_access_key=AWS_SECRET_ACCESS_KEY
				)
				s3 = session.resource('s3')
				print('l59 of models.py s3 read from try')
			
			except:
				s3 = boto3.resource('s3')
				print('l64 of models.py s3 read from except')

			bucket = s3.Bucket('asemolotion-blog')
			
			diff = '/'.join(diff.split('/')[3:])			
			# bucket.delete_object(diff)　ではなく、
			s3.Object('asemolotion-blog', diff).delete()
		super().delete()		

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
		custom = """
		<style type='text/css'>
		img {
			border: 1px solid gray;
		}
		</style>		
		"""
		# return custom + markdownify(self.content)
		return markdownify(self.content)
	
	def save(self, **kwargs):
		super().save(**kwargs)  # まず自分自身を保存しないと初回保存時にLinkFileが保存できない

		self.check_filelink_diffs()  # 保存する時にファイルのURLの保存

		super().save(**kwargs)  # 不要?




	def check_filelink_diffs(self):
		"""
		content内のファイルURLを抜き出して、保存する
		contentを編集してファイルURLが増減したら差分を保存、または削除する。


		"""

		# もともとあったfilepathを取り出して集合にする
		old_filelinks_queryset = self.filelink_set.values_list('filepath', flat=True)
		old_filelinks = set(list(old_filelinks_queryset)) or set(())
		
		# ![](linkurl)という画像のマークアップを全て取り出す

		# img_ptns = re.findall(
		# 	r'[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}\.(?:png|jpg|jpeg)',
		# 	# r'!.*\.(jpg|png|jpeg)',
		# 	# r'!\[\]\(https://asemolotion-blog\.s3\.amazonaws\.com/.*\.(jpeg|png|jpg)',
		# 	# r'\!\[\]\(.*(\.jpg|\.png|\.jpeg)',
		# 	self.content,
		# )

		# (?:...) non-capturing が大事　これがないと　| どっち、、ってなる短い方を取り出して終わられていた。
		img_ptns = re.findall(
			r'[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}\.(?:png|jpg|jpeg)',
			self.content,
		)

		print('this is img_ptns')
		print(img_ptns)

		# 画像マークアップからファイルパスを全て取り出す
		filelinks = []
		for ptn in img_ptns:
			
			if settings.DEBUG:
				# filelink = re.search(r'/\w+/\w+/.*\.(png|jpg|jpeg)', ptn).group()  # search()は最初の一個のみ。
				
				filelink = '/media/markdownx/' + ptn
				filelinks.append(filelink)
			else:  # aws s3の時
				# filelink = re.search(r'https://asemolotion-blog\.s3\.amazonaws\.com/markdownx/.*\.png').group()
				
				filelink = 'https://asemolotion-blog.s3.amazonaws.com/markdownx/' + ptn
				filelinks.append(filelink)

		print('this is filelinks ')
		print(filelinks)

		# filelinksになくて、old_filelinksにあるものを消す
		filelinks_diff = list(old_filelinks - set(filelinks))
		

		for diff in filelinks_diff:
			print('消すもの: ', diff)
			
			####################
			# FileLinkデータを消す
			###################

			FileLink.objects.filter(
				filepath=diff
			).delete()

			
			###################
			# ファイルの実体を消す
			###################

			if settings.DEBUG:
				# ローカルの時
				delete_filepath = os.path.abspath(os.path.join(settings.BASE_DIR, diff[1:]))  # diff もslashスタートなので、ルートと思ってjoinできない。
				print('ファイルパスは: ', delete_filepath)
				os.remove(delete_filepath)
			
			else:
				# s3のファイルを消す時
				
				try:
					# ローカルプロダクションの時は環境変数から取れないので、読み込む
					from conf.local_settings import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY
					session = boto3.Session(
						aws_access_key_id=AWS_ACCESS_KEY_ID,
						aws_secret_access_key=AWS_SECRET_ACCESS_KEY
					)
					s3 = session.resource('s3')
					print('l167 of models.py s3 read from try')
				
				except:
					s3 = boto3.resource('s3')
					print('l167 of models.py s3 read from except')

				bucket = s3.Bucket('asemolotion-blog')
				
				diff = '/'.join(diff.split('/')[3:])

				# diff = '/'.join(diff.split('/')[2:])
				# '/media/markdownx/b09354f2-24a2-481c-8593-39f781caf38a.png'
				# を 
				# 'markdownx/b09354f2-24a2-481c-8593-39f781caf38a.png'　にする。
				print(diff)
				
				# bucket.delete_object(diff)　ではなく、
				s3.Object('asemolotion-blog', diff).delete()
				
				print('finish delete_object')				

		# 今あるものはそのまま、追加分は追加の update_or_create()
		for filelink in filelinks:
			FileLink.objects.update_or_create(
				filepath = filelink,
				post = self
			)
			
		
		

