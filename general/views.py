from django.shortcuts import render
from django.views.generic import TemplateView


from blog.models import Post


class IndexView(TemplateView):
    template_name = 'general/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Postのリスト
        context['post_list'] = Post.objects.filter().order_by('-created_at')
        
        return context
    


class AboutView(TemplateView):
    template_name = 'general/about.html'

class ContactView(TemplateView):
    template_name = 'general/contact.html'