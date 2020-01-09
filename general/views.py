from django.shortcuts import render
from django.views.generic import TemplateView


from blog.models import Post, Project, Tag


class IndexView(TemplateView):
    template_name = 'general/index.html'

    POST_ITEM_COUNT = 7  # トップページで表示する記事リストのアイテム数
    PROJECT_ITEM_COUNT = 4


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Postのリスト
        context['post_list'] = Post.objects.filter().order_by('-created_at')[:self.POST_ITEM_COUNT]
        
        # Projectのリスト
        context['project_list'] = Project.objects.order_by('timestamp')[:self.PROJECT_ITEM_COUNT]

        return context
    


class AboutView(TemplateView):
    template_name = 'general/about.html'

class ContactView(TemplateView):
    template_name = 'general/contact.html'