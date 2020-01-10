from django.contrib import admin
from markdownx.admin import MarkdownxModelAdmin
from .models import Post, Tag, Project, FileLink


admin.site.register(Tag)
admin.site.register(Project)
admin.site.register(FileLink)

class CustomMarkdownxModelAdmin(MarkdownxModelAdmin):
    list_display = ('title', 'description', 'status', 'release_condition', 'post_type')
    
admin.site.register(Post, CustomMarkdownxModelAdmin)