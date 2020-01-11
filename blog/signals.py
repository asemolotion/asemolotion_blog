# for signal
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from .models import FileLink

# custom
import os
import boto3
from django.conf import settings

@receiver(pre_delete, sender=FileLink)
def delete_filelink_entity(sender, instance, using, **kwargs):
    """
    FileLinkにひもづくファイルをFileLink削除の時に削除する。

    Params:
        sender: The model class.
        instance: The actual instance being deleted.
        using: The database alias being used.
    """

    if settings.DEBUG:  
        # ローカルの時
        delete_filepath = os.path.abspath(os.path.join(settings.BASE_DIR, instance.filepath[1:]))  
        # filepathもslashスタートなので、ルートと思ってjoinできないので [1:]する
        os.remove(delete_filepath)
    
    else:
        # s3のファイルを消す時
        filepath = instance.filepath  # 削除するパス https://asemolotion-blog.s3...みたいなもの

        try:
            # ローカルプロダクションの時は環境変数から取れないので、読み込む
            from conf.local_settings import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY
            session = boto3.Session(
                aws_access_key_id=AWS_ACCESS_KEY_ID,
                aws_secret_access_key=AWS_SECRET_ACCESS_KEY
            )
            s3 = session.resource('s3')

        except:
            # heroku上の時は環境変数から読み込んでいるのでセッション作らなくていい。
            s3 = boto3.resource('s3')

        bucket = s3.Bucket('asemolotion-blog')
        
        filepath = '/'.join(filepath.split('/')[3:])	
        s3.Object('asemolotion-blog', filepath).delete()