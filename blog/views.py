from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import PermissionRequiredMixin
from .models import Post, Project, Tag

class BasePostListView(ListView):
    """
    ユーザの属性によって返すPostとProjectを制限する機能をもつBaseView
    """
    model = Post

    def get_post_queryset(self):
        # ユーザによって返すPostを制限する
        if self.request.user.is_superuser:
            queryset = self.model.objects.filter()  # all()にしたら連鎖させられないのでfilter()をつけとく。
        
        elif self.request.session.get('invitation_verification') == 'ok':
            queryset = self.model.objects.exclude(status='draft')

        else:
            queryset = self.model.objects.exclude(status='draft').exclude(release_condition='limited')
        
        return queryset

    def get_project_queryset(self):
        # ユーザによって返すProjectを制限する
        
        if self.request.user.is_superuser:
            queryset = Project.objects.filter()  # all()にしたら連鎖させられないのでfilter()をつけとく。
        
        elif self.request.session.get('invitation_verification') == 'ok':
            queryset = Project.objects.filter()

        else:
            queryset = Project.objects.exclude(release_condition='limited')
        
        return queryset        


class PostListView(BasePostListView):
    """ 記事のリストビュー　
    Article or ShortCode　のフィルタ
    ページング　
    があり
    """

    model = Post
    paginate_by = 3
    template_name = 'blog/list.html'

    def get_queryset(self):
        posts = super().get_post_queryset()

        if self.request.GET.get('q') == 'article':
            return posts.filter(post_type='article')
        elif self.request.GET.get('q') == 'short_code':
            return posts.filter(post_type='short_code')
        else:
            return posts

    
    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['project_list'] = self.get_project_queryset()
        context['tag_list'] = Tag.objects.all()  # Tagは全て返却
        return context


class PostDetailView(PermissionRequiredMixin, DetailView):
    """ 
    投稿(Post)の詳細ページ。ユーザの属性で公開、非公開の条件わけあり。 
    条件は PermissionRequiredMixin　で設定。
    """
    
    model = Post
    template_name = 'blog/detail.html'

    login_url = reverse_lazy('general:index')  # permissionがFalseの時にリダイレクトされるURL

    def has_permission(self):
        post = self.model.objects.filter(pk=self.kwargs['pk']).first()

        if post.release_condition == 'limited':  # 'limited'のものはsuperuserかverificationのみ。
            if self.request.user.is_superuser:
                return True
            
            elif self.request.session.get('invitation_verification') == 'ok':
                return True

            else:
                return False
        
        else:  # publicのものは全て公開。
            return True



class ProjectView(PermissionRequiredMixin, BasePostListView):
    """
    あるプロジェクトに属するPostのリストビュー。そのプロジェクト自体がLIMITEDならアクセスできない。
    ページング　
    があり    
    """
    paginate_by = 3

    template_name = 'blog/project.html'
    slug = ''

    login_url = reverse_lazy('general:index')  # permissionがFalseの時にリダイレクトされるURL
    permission_denied_message = 'you did not confirmed yet. please check your email.'
    
    def has_permission(self):
        """ ページの表示か否かの条件分岐 """
        project = Project.objects.filter(
            slug=self.kwargs.get('project_slug')
        ).first()

        if project.release_condition == 'limited':
            if self.request.user.is_superuser:
                return True
            
            elif self.request.session.get('invitation_verification') == 'ok':
                return True

            else:
                return False
        else:  # publicのものは全て公開していい。
            return True        


    def get_queryset(self):
        queryset = super().get_post_queryset()

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
    ページング　
    があり    
    """
    paginate_by = 3
    
    template_name = 'blog/tag.html'
    slug = ''

    def get_queryset(self):
        queryset = super().get_post_queryset()

        self.slug = self.kwargs.get('tag_slug')
        queryset = queryset.filter(tags__slug=self.slug)  # M2Mの1個をだす条件のクエリ
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        tag = Tag.objects.filter(slug=self.slug).first()
        context['tag'] = tag

        return context