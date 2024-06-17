import os

HDFC_LOG_HANDLER = ['default', 'gelf']

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# This setting level variable is of type boolean and if set to true the Mobile User Request Logging
# takes place otherwise it doesn't
MOBILE_USER_LOGGING = True

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s || [%(levelname)s] || %(name)s || %(message)s'
        },
        'simple': {
            #'[%(asctime)s] - \n %(message)s \n================= \n',
            'datefmt': '%d-%m-%Y %H:%M:%S'
        },
    },
    'handlers': {
        'default': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(BASE_DIR, '../logs/api_hdfclife.log'),
            'maxBytes': 1024*1024*50,
            'backupCount': 10,
            'formatter': 'standard',
        },
        'stream': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'standard',
        },
        'gelf': {
            'class': 'graypy.GELFTCPHandler',
            'host': 'localhost',
            'port': 12201,
        },
        'user_request': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(BASE_DIR, '../logs/user_request.log'),
            'maxBytes': 1024 * 1024 * 50,
            'backupCount': 10,
            'formatter': 'simple',
        },
        'cms_info': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(BASE_DIR, '../logs/cms_info.log'),
            'maxBytes': 1024*1024*50,
            'backupCount': 10,
            'formatter': 'simple',
        },
        'cms_error': {
            'level': 'ERROR',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(BASE_DIR, '../logs/cms_error.log'),
            'maxBytes': 1024*1024*50,
            'backupCount': 10,
            'formatter': 'simple',
        },
        'cms_warn': {
            'level': 'WARNING',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(BASE_DIR, '../logs/cms_warn.log'),
            'maxBytes': 1024*1024*50,
            'backupCount': 10,
            'formatter': 'simple',
        },
        'cms_debug': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(BASE_DIR, '../logs/cms_debug.log'),
            'maxBytes': 1024*1024*50,
            'backupCount': 10,
            'formatter': 'simple',
        },
    },
    'loggers': {
        'default': {
            'handlers': HDFC_LOG_HANDLER,
            'level': 'DEBUG',
            'propagate': True
        },
        'cms_info': {
            'handlers': ['cms_info'],
            'level': 'DEBUG',
            'propagate': True
        },
        'cms_error': {
            'handlers': ['cms_error'],
            'level': 'DEBUG',
            'propagate': True
        },
        'cms_warn': {
            'handlers': ['cms_warn'],
            'level': 'DEBUG',
            'propagate': True
        },
        'cms_debug': {
            'handlers': ['cms_debug'],
            'level': 'DEBUG',
            'propagate': True
        },
        'django.request': {
            'handlers': HDFC_LOG_HANDLER,
            'level': 'ERROR',
            'propagate': False
        },
    }
}