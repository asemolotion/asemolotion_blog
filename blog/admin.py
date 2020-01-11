from django.contrib import admin

from markdownx.models import MarkdownxField
from markdownx.admin import MarkdownxModelAdmin
from markdownx.widgets import AdminMarkdownxWidget

from .models import Post, Tag, Project, FileLink


admin.site.register(Tag)
admin.site.register(Project)
admin.site.register(FileLink)

class CustomAdminMarkdownxWidget(AdminMarkdownxWidget):
	
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.attrs={'cols': 50, 'rows': 30}
		"""
		forms.TextAreaのattrsを書き換えている。
		"""
	

class CustomMarkdownxModelAdmin(MarkdownxModelAdmin):
	list_display = ('title', 'description', 'status', 'release_condition', 'post_type')
	
	formfield_overrides = {
		   MarkdownxField: {'widget': CustomAdminMarkdownxWidget}
	} 
   
	# class Meta:
	# 	widgets = {
	# 		'text': MarkdownxWidget(attrs={
	# 			# 'class': 'textarea',
	# 			# 'style': 'height:400px;',
	# 			# 'rows':50, 
	# 			# 'cols':40
	# 			}),
	# 	}        

admin.site.register(Post, CustomMarkdownxModelAdmin)