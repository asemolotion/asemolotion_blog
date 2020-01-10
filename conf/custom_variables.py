import os
from django.conf import settings

if settings.DEBUG:
    # ローカル
    from .local_settings import INVITATION_CODE_VAL
    INVITATION_CODE = INVITATION_CODE_VAL

else:
    # heroku
    INVITATION_CODE = os.environ.get('INVITATION_CODE')