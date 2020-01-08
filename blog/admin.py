from django.contrib import admin
from markdownx.admin import MarkdownxModelAdmin
from .models import Post, Tag

admin.site.register(Tag)

class CustomMarkdownxModelAdmin(MarkdownxModelAdmin):
    list_display = ('title', 'description')
    
admin.site.register(Post, CustomMarkdownxModelAdmin)