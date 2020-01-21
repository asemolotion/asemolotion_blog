from django.urls import path 
from .views import *

app_name = 'blog'

urlpatterns = [
    path('', PostListView.as_view(), name='list'),  # 記事のリストビュー
    path('<int:pk>/', PostDetailView.as_view(), name='detail'),  # 記事の詳細ビュー
    path('project/<slug:project_slug>/', ProjectView.as_view(), name='project'), # プロジェクトでフィルタされた記事リスト
    path('tag/<slug:tag_slug>/', TagView.as_view(), name='tag'),  # タグでフィルタされた記事リスト
]