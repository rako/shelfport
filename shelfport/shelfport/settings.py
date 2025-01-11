from .settings_common import *

# 本番運用環境用にセキュリティキーを生成し環境変数から読み込む
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')

# デバッグモードを有用にするかどうか（本番環境では必ずFalseにする）
DEBUG = False

# 許可するホスト名のリスト
ALLOWED_HOSTS = [os.environ.get('ALLOWED_HOSTS')]

# 静的ファイルを配置する場所
STATIC_ROOT = '/usr/share/nginx/html/static'

# Amazon SES関連設定
AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
EMAIL_BACKEND = 'django_ses.SESBackend'
# AWSのリージョンがus-east-1(バージニア北部)以外の場合は設定が必要
# AWS_SES_REGION_NAME = 'us-west-2'
# AWS_SES_REGION_ENDPOINT = 'email.us-west-2.amazonaws.com'

# ロギング設定
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    
    # ロガーの設定
    'loggers': {
        # Djangoが利用するロガー
        'django': {
            'handlers': ['file'],
            'level': 'INFO',
        },
        # shelfportアプリケーションが利用するロガー
        'shelfport': {
            'handlers': ['file'],
            'level': 'INFO',
    },

    # ハンドラの設定
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': os.path.join(BASE_DIR, 'logs/django.log'),
            'formatter': 'prod',
            'when': 'D', #ログローテーション（新しいファイルへの切り替え間隔の単位（D＝日））
            'interval': 1, #ログローテーション間隔（1日ごと）
            'backupCount': 7, #バックアップファイルの保持数
        },
    },

    # フォーマッタの設定
    'formatters': {
        'prod': {
            'format': '\t'.join([
                '%(asctime)s',
                '[%(levelname)s]',
                '%(pathname)s(Line:%(lineno)d)',
                '%(message)s'
            ])
        },
    }
}
}