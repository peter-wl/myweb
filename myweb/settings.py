# -*- coding:utf-8 -*-
"""
Django settings for myweb project.

Generated by 'django-admin startproject' using Django 1.8.17.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'qmb_(ecv)1mq3av_f-necld!bp37er#+m4-up3d7v69=n#)@0u'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']
AUTH_USER_MODEL = 'user.UserProfile'


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'accounts',
    'index',
    'user',
    'asset',
    'workorder',
    'pure_pagination',
    'service',
)
PAGINATION_SETTINGS={
    'PAGE_RANGE_DISPLAYED':2, #每页显示10行
    'MARGIN_PAGES_DISPLAYED':2,#首尾只显示两条连续
    'SHOW_FIRST_PAGE_WHEN_INVALID':True,#如果页码不存在只显示首页
}



MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)

ROOT_URLCONF = 'myweb.urls'

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

WSGI_APPLICATION = 'myweb.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases
#
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#     }
# }
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'myweb',
        'USER': 'wl',
        'PASSWORD': 'wl123',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'en-us'

# TIME_ZONE = 'UTC'
TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = True

LOGIN_URL = '/login/'


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS=(
    os.path.join(BASE_DIR,'static'),
)

# ADMINS = (
# # ('peter.wang','becauseofni@sina.com'),
# ('peter.wang','wangliang@feinno.com'),
# )
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST= 'smtp.feinno.com'#QQ邮箱SMTP服务器(邮箱需要开通SMTP服务)
EMAIL_PORT= 587 #QQ邮箱SMTP服务端口
EMAIL_HOST_USER = 'wangliang@feinno.com' #我的邮箱帐号
EMAIL_HOST_PASSWORD = 'Feiliao2012@' #授权码
# EMAIL_SUBJECT_PREFIX = 'myweb' #为邮件标题的前缀,默认是'[django]'
EMAIL_USE_TLS = False #开启安全链接
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST= 'smtp.sina.com'#QQ邮箱SMTP服务器(邮箱需要开通SMTP服务)
# EMAIL_PORT= 25 #QQ邮箱SMTP服务端口
# EMAIL_HOST_USER = 'becauseofni@sina.com' #我的邮箱帐号
# EMAIL_HOST_PASSWORD = 'Feiliao2014!' #授权码
# EMAIL_SUBJECT_PREFIX = 'myweb' #为邮件标题的前缀,默认是'[django]'
# EMAIL_USE_TLS = True #开启安全链接
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER #设置发件人
LOGGING = {
    "version": 1,
    'disable_existing_loggers': False,
    "loggers": {
        "myweb": {
            "level": "DEBUG",
            "handlers": ["myweb_file_handler",'mail'],
            # 'propagate': True,
            # "handlers": ["console_handler", "myweb_file_handler"],
        },
        # "django": {
        #     "level": "DEBUG",
        #     "handlers": [ "django_handler"],
        # },

    },
    "handlers":{
        "console_handler": {
            "class": "logging.StreamHandler",
            "formatter": 'simple'
        },
        "myweb_file_handler": {
            "class": "logging.FileHandler",
            "filename": os.path.join(BASE_DIR, "logs", "myweb.log"),
            "formatter": "myweb"
        },
        "django_handler": {
            "class": "logging.FileHandler",
            "filename": os.path.join(BASE_DIR, "logs", "django.log"),
            "formatter": "myweb"
        },
        # 'mail_admins': {
        #     'level': 'ERROR',
        #     'class': 'django.utils.log.AdminEmailHandler',
        #     'formatter': 'myweb',
        #     # 'include_html':False,
        # }
        'mail':{
            'class':'logging.handlers.SMTPHandler',
            'level':'ERROR',
            'formatter':'myweb',
            'mailhost':('smtp.feinno.com',587),
            'fromaddr':'wangliang@feinno.com',  #发件人
            'toaddrs':['becauseofni@sina.com'], #收件人
            'subject':'myweb error message',    #邮件标题
            'credentials':('wangliang','Feiliao2012@')  #发件人 用户名密码
        }
    },

    "formatters": {
        "myweb": {
            "format": "%(asctime)s %(pathname)s %(lineno)d [%(levelname)s] %(message)s"
        },
        "simple": {
            "format": "%(asctime)s %(levelname)s %(message)s"
        }
    },
}
