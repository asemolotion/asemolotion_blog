from django.urls import path
from .views import *

app_name = 'general'  

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('about/', AboutView.as_view(), name='about'),
    path('contact/', ContactView.as_view(), name='contact'),

    path('verify_invitaion/', verify_invitation, name='verify_invitation'),
    path('clear_invitation/', clear_invitation, name='clear_invitation'),    
]