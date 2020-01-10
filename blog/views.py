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


class ProjectView(ListView):
    template_name = 'blog/project.html'
    slug = ''

    def get_queryset(self):

        if self.request.user.is_superuser:
            queryset = Post.objects
        
        elif self.request.session.get('invitation_verification') == 'ok':
            queryset = Post.objects.exclude(status='draft')

        else:
            queryset = Post.objects.exclude(status='draft').exclude(release_condition='limited')


        self.slug = self.kwargs.get('project_slug')
        queryset = queryset.filter(project__slug=self.slug)
        
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        project = Project.objects.filter(slug=self.slug).first()
        context['project'] = project

        return context
    


class TagView(ListView):
    template_name = 'blog/tag.html'
    slug = ''

    def get_queryset(self):

        self.slug = self.kwargs.get('tag_slug')
        queryset = Post.objects.filter(tags__slug=self.slug)  # M2Mの1個をだす条件のクエリ
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        tag = Tag.objects.filter(slug=self.slug).first()
        context['tag'] = tag

        return context