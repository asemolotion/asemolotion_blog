from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Post, Project, Tag

class BlogListView(ListView):
    model = Post
    template_name = 'blog/list.html'


    def get_queryset(self):
        if self.request.user.is_superuser:
            return Post.objects.all()
        
        elif self.request.session.get('invitation_verification') == 'ok':
            return Post.objects.exclude(status='draft')

        else:
            return Post.objects.exclude(status='draft').exclude(release_condition='limited')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['project_list'] = Project.objects.all()
        context['tag_list'] = Tag.objects.all()
        return context

class BlogDetailView(DetailView):
    model = Post
    template_name = 'blog/detail.html'
