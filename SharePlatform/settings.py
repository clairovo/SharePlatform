"""
Django settings for SharePlatform project.

Generated by 'django-admin startproject' using Django 3.1.3.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""
import os
from pathlib import Path
from mongoengine import connect

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# logging配置
log_file = os.path.join(BASE_DIR,'logs')
log_file_path = os.path.join(log_file, 'all.log')
if not os.path.exists(log_file):
    os.mkdir(log_file)
    with open(log_file_path,'w') as fp:
        pass
    # os.mknod(log_file_path)  # 创建空文件

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        # 日志格式
        'standard': {
            'format': '%(asctime)s  [%(levelname)s] %(thread)d --- [%(threadName)s] [%(name)s:%(lineno)d]'
                      '[%(module)s:%(funcName)s]: %(message)s'
        }
    },
    'filter': {

    },
    'handlers': {
        'mail_admins': {  # 它将用邮件发送ERROR（和更高级）的消息到站点管理员
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
            'include_html': True,
        },
        'default': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': log_file_path,  # 日志输出文件
            'maxBytes': 1024 * 1024 * 5,  # 文件大小
            'backupCount': 5,  # 备份份数
            'formatter': 'standard',  # 使用哪种formatters日志格式
        },
        'error': {
            'level': 'ERROR',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': log_file_path,
            'maxBytes': 1024 * 1024 * 5,
            'backupCount': 5,
            'formatter': 'standard',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'standard'
        },
        'request_handler': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': log_file_path,
            'maxBytes': 1024 * 1024 * 5,
            'backupCount': 5,
            'formatter': 'standard',
        },
        'scprits_handler': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': log_file_path,
            'maxBytes': 1024 * 1024 * 5,
            'backupCount': 5,
            'formatter': 'standard',
        }
    },
    'loggers': {
        # 'django': {
        #     'handlers': ['default', 'console'],  # 来自上面定义的handlers内容
        #     'level': 'INFO',
        #     'propagate': False  # 是否继承父类的log信息
        # },
        'scripts': {
            'handlers': ['scprits_handler'],
            'level': 'INFO',
            'propagate': False
        },
        # login,resource等应用操作的view.py 对应的日志
        'resource.views': {
            'handlers': ['default', 'error'],
            'level': 'INFO',
            'propagate': True
        },
        'login.views': {
            'handlers': ['default', 'error'],
            'level': 'INFO',
            'propagate': True
        },
        'course.views': {
            'handlers': ['default', 'error'],
            'level': 'INFO',
            'propagate': True

        },
        'user.views': {
            'handlers': ['default', 'error'],
            'level': 'INFO',
            'propagate': True

        },
        'sourceDns.webdns.util': {
            'handlers': ['error'],
            'level': 'ERROR',
            'propagate': True
        },
        # 记录请求日志
        'django.request': {
           'handlers': ['request_handler'],
           'level': 'DEBUG',
           'propagate': False,
          },
    }
}


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '=w(p4-&-%wa#0&l7((9b!k+)6wi7jg3$vptj0qdzyy=n+df$v+'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework_mongoengine',
    'login.apps.LoginConfig',
    'resource.apps.ResourceConfig',
    'user',
    'course',
    'corsheaders'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
     'corsheaders.middleware.CorsMiddleware', ## 跨域中间件
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'SharePlatform.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'SharePlatform.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': 'django',  # 数据库名
#         'HOST': '127.0.0.1',  # 数据库地址，本机 ip 地址 127.0.0.1
#         'PORT': 3306,  # 端口
#         'USER': 'root',  # 数据库用户名
#         'PASSWORD': '980920',  # 数据库密码
#     }
}
connect('test',host='127.0.0.1', port=27017)  # 连接数据库的名称

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        #'login.login_token.AdminPermission',
        'login.login_token.Authenticated',
    ),
}

# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = (
    os.path.join(os.path.join(BASE_DIR, 'static')),
)

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')    # 配置media文件，用于记录日志/存放文件
## 跨域设置
CORS_ALLOW_CREDENTIALS = True
CORS_ORIGIN_ALLOW_ALL = True
CORS_ORIGIN_WHITELIST = ()

CORS_ALLOW_METHODS = (
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
    'VIEW',
)

CORS_ALLOW_HEADERS = (
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
)
