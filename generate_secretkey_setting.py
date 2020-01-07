"""
SECRET_KEYを生成するスクリプト

参考: https://qiita.com/haessal/items/abaef7ee4fdbd3b218f5

githubからcloneした時に　SECRET_KEYがないので、
このスクリプトで生成して、local_settings.pyを作り、そこに書き込むようにする。

$ git clone <this remote repo>
$ python generate_secretkey_setting.py > local_settings.py

"""

from django.core.management.utils import get_random_secret_key

secret_key = get_random_secret_key()
text = 'SECRET_KEY = \'{0}\''.format(secret_key)
print(text)
