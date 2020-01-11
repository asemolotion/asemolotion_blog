from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import PermissionRequiredMixin
from .models import Post, Project, Tag

class BasePostListView(ListView):
    """
    ユーザの属性によって返すPostを制限する機能をもつBaseView
    """    
    model = Post

    def get_queryset(self):
        if self.request.user.is_superuser:
            queryset = self.model.objects.filter()  # all()にしたら連鎖させられないのでfilter()をつけとく。
        
        elif self.request.session.get('invitation_verification') == 'ok':
            queryset = self.model.objects.exclude(status='draft')

        else:
            queryset = self.model.objects.exclude(status='draft').exclude(release_condition='limited')
        
        return queryset


class PostListView(BasePostListView):
    model = Post
    template_name = 'blog/list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['project_list'] = Project.objects.all()
        context['tag_list'] = Tag.objects.all()
        return context


class PostDetailView(PermissionRequiredMixin, DetailView):
    """ 投稿(Post)の詳細ページ。ユーザの属性で公開、非公開の条件分岐。 """
    
    model = Post
    template_name = 'blog/detail.html'

    login_url = reverse_lazy('general:index')  # permissionがFalseの時にリダイレクトされるURL

    def has_permission(self):
        post = self.model.objects.filter(pk=self.kwargs['pk']).first()

        if post.release_condition == 'limited':
            if self.request.user.is_superuser:
                return True
            
            elif self.request.session.get('invitation_verification') == 'ok':
                return True

            else:
                return False
        else:  # publicのものは全て公開していい。
            return True



class ProjectView(BasePostListView):
    """
    あるプロジェクトに属するPostのリストビュー
    """
    template_name = 'blog/project.html'
    slug = ''

    def get_queryset(self):
        queryset = super().get_queryset()

        self.slug = self.kwargs.get('project_slug')
        queryset = queryset.filter(project__slug=self.slug)
        
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        project = Project.objects.filter(slug=self.slug).first()
        context['project'] = project

        return context
    

class TagView(BasePostListView):
    """
    あるタグをもつPostのリストビュー
    """
    template_name = 'blog/tag.html'
    slug = ''

    def get_queryset(self):
        queryset = super().get_queryset()

        self.slug = self.kwargs.get('tag_slug')
        queryset = queryset.filter(tags__slug=self.slug)  # M2Mの1個をだす条件のクエリ
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        tag = Tag.objects.filter(slug=self.slug).first()
        context['tag'] = tag

        return context