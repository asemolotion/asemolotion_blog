from django.urls import path 
from .views import *

app_name = 'blog'

urlpatterns = [
    path('', PostListView.as_view(), name='list'),
    path('<int:pk>/', PostDetailView.as_view(), name='detail'),
    path('project/<slug:project_slug>/', ProjectView.as_view(), name='project'),
    path('tag/<slug:tag_slug>/', TagView.as_view(), name='tag'),
]