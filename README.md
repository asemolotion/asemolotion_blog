# asemolotion_blog
remote of asemolotion_blog working directory.

this is repository of my blog site in 2020~


### ローカルで準備するもの
local_settings.py
```
import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = <string: SECRET_KEY>

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

DEBUG = True

## LocalProduction Vars
AWS_ACCESS_KEY_ID = <string: AWS_ACCESS_KEY_ID>
AWS_SECRET_ACCESS_KEY = <string: AWS_SECRET_ACCESS_KEY>


DATABASE_URL = <string:herokuのpostgres URL>

PG_NAME = <string:DB name>
PG_USER = <string:DB user>
PG_PASSWORD = <string:DB password>
PG_HOST = <string:DB host>
PG_PORT = <string:DB port>

## My Custom Vars
INVITATION_CODE_VAL = <string:自由に決める招待コード>
```

local_production_settings.py
```
# import 順番も大事。まず一般設定をimportして、ローカルのものをimport,そして上書き。
from .settings import *
from .local_settings import *

AWS_ACCESS_KEY_ID = AWS_ACCESS_KEY_ID
AWS_SECRET_ACCESS_KEY = AWS_SECRET_ACCESS_KEY

# これがあればMEDIA_ROOTは読まない
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
AWS_STORAGE_BUCKET_NAME = 'asemolotion-blog'
AWS_DEFAULT_ACL = None

# URLがexpireになるやつじゃなくする
AWS_QUERYSTRING_EXPIRE = '157784630'
AWS_S3_CUSTOM_DOMAIN = "https://%s.s3.amazonaws.com" % AWS_STORAGE_BUCKET_NAME

DATABASES['default'] = {
    'ENGINE': 'django.db.backends.postgresql_psycopg2',
    'NAME': PG_NAME,
    'USER': PG_USER,
    'PASSWORD': PG_PASSWORD,
    'HOST': PG_HOST,
    'PORT': PG_PORT,
}

DEBUG = True  # => STATIC_ROOTを使う？ 

```
