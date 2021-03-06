from django.views.generic import TemplateView

from django.shortcuts import render
from django.urls import reverse
from django.shortcuts import redirect

from blog.models import Post, Project, Tag


class IndexView(TemplateView):
    template_name = 'general/index.html'

    POST_ITEM_COUNT = 7  # トップページで表示する記事リストのアイテム数
    PROJECT_ITEM_COUNT = 4


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Postのリスト 公開かつ全員に公開のみ。
        context['post_list'] = \
            Post.objects\
                .filter(status='released')\
                .filter(release_condition='public')\
                .order_by('-created_at')[:self.POST_ITEM_COUNT]
        
        # Projectのリスト
        context['project_list'] = Project.objects\
            .filter(release_condition='public')\
            .order_by('timestamp')[:self.PROJECT_ITEM_COUNT]

        # Tagのリスト
        context['tag_list'] = Tag.objects.all()

        return context
    


class AboutView(TemplateView):
    template_name = 'general/about.html'

class ContactView(TemplateView):
    template_name = 'general/contact.html'



from conf.custom_variables import INVITATION_CODE
def verify_invitation(request):
    """
    招待コード認証を確認するビュー
    """
    code = request.POST.get('code')

    if code == INVITATION_CODE:
        # 招待コードが成功したら以下のセッションキーをつける。
        request.session['invitation_verification'] = 'ok'

    return redirect(reverse('general:index'))

def clear_invitation(request):
    """
    招待コード認証を解消するコマンドのビュー
    """
    if request.session.get('invitation_verification'):
        del request.session['invitation_verification']
    return redirect(reverse('general:index'))