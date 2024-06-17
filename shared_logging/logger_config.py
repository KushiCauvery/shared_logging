import os
import logging
from logging.handlers import RotatingFileHandler
from django.conf import settings

# Ensure logs directory exists
LOG_DIR = os.path.join(settings.BASE_DIR, 'logs')
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

# Define log file paths
LOG_FILE_API = os.path.join(LOG_DIR, 'api_hdfclife.log')
LOG_FILE_USER_REQUEST = os.path.join(LOG_DIR, 'user_request.log')
LOG_FILE_CMS_INFO = os.path.join(LOG_DIR, 'cms_info.log')
LOG_FILE_CMS_ERROR = os.path.join(LOG_DIR, 'cms_error.log')
LOG_FILE_CMS_WARN = os.path.join(LOG_DIR, 'cms_warn.log')
LOG_FILE_CMS_DEBUG = os.path.join(LOG_DIR, 'cms_debug.log')

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s || [%(levelname)s] || %(name)s || %(message)s',
        },
        'simple': {
            'format': '[%(asctime)s] - %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S',
        },
    },
    'handlers': {
        'default': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': LOG_FILE_API,
            'maxBytes': 1024*1024*50,  # 50 MB
            'backupCount': 10,
            'formatter': 'standard',
        },
        'user_request': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': LOG_FILE_USER_REQUEST,
            'maxBytes': 1024 * 1024 * 50,
            'backupCount': 10,
            'formatter': 'simple',
        },
        'cms_info': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': LOG_FILE_CMS_INFO,
            'maxBytes': 1024*1024*50,
            'backupCount': 10,
            'formatter': 'simple',
        },
        'cms_error': {
            'level': 'ERROR',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': LOG_FILE_CMS_ERROR,
            'maxBytes': 1024*1024*50,
            'backupCount': 10,
            'formatter': 'simple',
        },
        'cms_warn': {
            'level': 'WARNING',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': LOG_FILE_CMS_WARN,
            'maxBytes': 1024*1024*50,
            'backupCount': 10,
            'formatter': 'simple',
        },
        'cms_debug': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': LOG_FILE_CMS_DEBUG,
            'maxBytes': 1024*1024*50,
            'backupCount': 10,
            'formatter': 'simple',
        },
        # Add other handlers as needed
    },
    'loggers': {
        'default': {
            'handlers': ['default'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'cms_info': {
            'handlers': ['cms_info'],
            'level': 'INFO',
            'propagate': True,
        },
        'cms_error': {
            'handlers': ['cms_error'],
            'level': 'ERROR',
            'propagate': True,
        },
        'cms_warn': {
            'handlers': ['cms_warn'],
            'level': 'WARNING',
            'propagate': True,
        },
        'cms_debug': {
            'handlers': ['cms_debug'],
            'level': 'DEBUG',
            'propagate': True,
        },
        # Add other loggers as needed
    },
}

logging.config.dictConfig(LOGGING)
