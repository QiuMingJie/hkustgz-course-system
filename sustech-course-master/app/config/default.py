import sys

# Server config
SERVER_NAME = None
DEBUG = False
for arg in sys.argv:
    if arg == '-d':
        DEBUG = True

SECRET_KEY = 'secret-key'
EMAIL_CONFIRM_SECRET_KEY = 'secret-key'
PASSWORD_RESET_SECRET_KEY = 'secret-key'


# available languages
LANGUAGES = {
    'en': 'English',
    'zh': '中文'
}


# SQL config
SQLALCHEMY_DATABASE_URI = 'mysql+mysqldb://root:@localhost/icourse?charset=utf8mb4'
SQLALCHEMY_TRACK_MODIFICATIONS = False

# Flask mail
MAIL_SERVER = 'localhost'
MAIL_PORT = 25
MAIL_USE_TLS = False
MAIL_USE_SSL = False
MAIL_DEBUG = DEBUG
MAIL_USERNAME = None
MAIL_PASSWORD = None
MAIL_DEFAULT_SENDER = 'support@icourse.club'
MAIL_MAX_EMAILS = None
# MAIL_SUPPRESS_SEND =
MAIL_ASCII_ATTACHMENTS = False

# Upload config
UPLOAD_FOLDER = '/srv/ustc-course/uploads'
# Alowed extentsions for a filetype
# for example 'image': set(['png', 'jpg', 'jpeg', 'gif'])
ALLOWED_EXTENSIONS = {
    'image': set(['png', 'jpg', 'jpeg', 'gif']),
    'file': set('7z|avi|csv|doc|docx|flv|gif|gz|gzip|jpeg|jpg|mov|mp3|mp4|mpc|mpeg|mpg|ods|odt|pdf|png|ppt|pptx|ps|pxd|rar|rtf|tar|tgz|txt|vsd|wav|wma|wmv|xls|xlsx|xml|zip'.split('|')),
}
MAX_CONTENT_LENGTH = 100 * 1024 * 1024


IMAGE_PATH = 'uploads/images'


# Debugbar Settings
# Enable the profiler on all requests
DEBUG_TB_PROFILER_ENABLED = False
# Enable the template editor
DEBUG_TB_TEMPLATE_EDITOR_ENABLED = False
DEBUG_TB_INTERCEPT_REDIRECTS = False
DEBUG_TB_ENABLED = False

# OAUTH Settings
OAUTH = {  # 配置参数，如果没有设置正确，OAuth流程就会失败
    "client_id":  '',
    "client_secret": '',
    "redirect_uri": '',
    "scope": 'profile',  # 表示OAuth请求授权的范围
    "auth_url": '',
    "token_url": '',
    "api_url": ''
}

# Cloudflare Turnstile Settings
RECAPTCHA_SITE_KEY = '0x4AAAAAABBpSp3f59fEQteR'  # 这是一个示例密钥，需要替换为实际的密钥
RECAPTCHA_SECRET_KEY = '0x4AAAAAABBpSthFZxGikevwf9aY-kHtFMo'  # 这是一个示例密钥，需要替换为实际的密钥

# S3 Config
S3_CONFIG = None
S3_BUCKET_NAME = None
S3_REGION = None
