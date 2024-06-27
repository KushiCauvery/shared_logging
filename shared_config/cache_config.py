# # DEFAULT_CACHE_BACKEND = 'django.core.cache.backends.filebased.FileBasedCache'
# # DEFAULT_CACHE_LOCATION = 'application.cache'

# # Uncomment this settings for Rediscache
# DEFAULT_CACHE_BACKEND = 'django_redis.cache.RedisCache'
# DEFAULT_CACHE_LOCATION = 'redis://127.0.0.1:6379/1'

# API_CACHE_BACKEND = 'django_redis.cache.RedisCache'
# API_CACHE_LOCATION = 'redis://127.0.0.1:6379/3'

# API_THROTTLE_CACHE_BACKEND = 'django_redis.cache.RedisCache'
# API_THROTTLE_CACHE_LOCATION = 'redis://127.0.0.1:6379/5'

# POST_API_CACHE_BACKEND = 'django_redis.cache.RedisCache'
# POST_API_CACHE_LOCATION = 'redis://127.0.0.1:6379/6'
# POST_API_CACHE = "post_api"

# BRANDSITE_BACKEND_CACHE = 'django_redis.cache.RedisCache'
# BRANDSITE_BACKED_CACHE_LOCATION = 'redis://127.0.0.1:6379/9'

# REDIRECTION_CACHE = "redirection"
# REDIRECTION_CACHE_BACKEND = 'django_redis.cache.RedisCache'
# REDIRECTION_CACHE_LOCATION = 'redis://127.0.0.1:6379/2'

# # Cache settings
# CACHES = {
#     'default': {
#         'BACKEND': DEFAULT_CACHE_BACKEND,
#         'LOCATION': DEFAULT_CACHE_BACKEND,
#     },
#     "api": {
#         "BACKEND": API_CACHE_BACKEND,
#         "LOCATION": API_CACHE_LOCATION,
#         "OPTIONS": {
#             "CLIENT_CLASS": "django_redis.client.DefaultClient"
#         },
#         "KEY_PREFIX": "hdfclife"
#     },
#     "api_v1": {
#         'BACKEND': 'django_redis.cache.RedisCache',
#         'LOCATION': API_CACHE_LOCATION,
#         "OPTIONS": {
#             "CLIENT_CLASS": "django_redis.client.DefaultClient"
#         },
#         "KEY_PREFIX": "hdfclife"
#     },
#     'api_throttle': {
#         'BACKEND': API_THROTTLE_CACHE_BACKEND,
#         'LOCATION': API_THROTTLE_CACHE_LOCATION,
#     },
#     'brandsite_backend': {
#         'BACKEND': BRANDSITE_BACKEND_CACHE,
#         'LOCATION': BRANDSITE_BACKED_CACHE_LOCATION,
#         'TIMEOUT': None,
#     },
#     POST_API_CACHE: {
#         'BACKEND': POST_API_CACHE_BACKEND,
#         'LOCATION': POST_API_CACHE_LOCATION,
#         'TIMEOUT': 60 * 60 * 1,                     # Timeout of 1 Hr
#     },
#     REDIRECTION_CACHE: {
#         'BACKEND': REDIRECTION_CACHE_BACKEND,
#         'LOCATION': REDIRECTION_CACHE_LOCATION,
#         'TIMEOUT': None,                            # Never expire redirection keys
#     },
# }


# # cache config settings
# ENABLE_CACHE = True
# MAX_CACHE_EXPIRE_TIME = 3600
# SINGLE_DAY_CACHE_TIMEOUT = 60 * 60 * 24  # 1 days
# SEVEN_DAYS_CACHE_TIMEOUT = 60 * 60 * 24 * 7  # 7 days
# HALF_HOUR_CACHE_TIMEOUT = 60 * 60 * 0.5
# ONE_HOUR_CACHE_TIMEOUT = 60 * 60 * 1

# VIEWCOUNT_CACHE_TIMEOUT = 60 * 60 * 24 # 1 day

# MANUAL_RECENT_SEARCH_TERMS_TIMOUT = 60 * 60 * 24 * 30  # One Month
# MANUAL_TRENDING_SEARCH_TERMS_TIMOUT = 60 * 60 * 24 * 7  # One Week
# -------------------------------------------------------------------------------------
# sonata-custom
import environ

# Initialize environment variables
env = environ.Env()
environ.Env.read_env()

# Load Redis settings from environment variables
REDIS_HOST = env('REDIS_HOST', default='127.0.0.1')
REDIS_PORT = env('REDIS_PORT', default='6379')
REDIS_DB_DEFAULT = env('REDIS_DB_DEFAULT', default='1')
REDIS_DB_API = env('REDIS_DB_API', default='3')
REDIS_DB_API_THROTTLE = env('REDIS_DB_API_THROTTLE', default='5')
REDIS_DB_POST_API = env('REDIS_DB_POST_API', default='6')
REDIS_DB_BRANDSITE_BACKEND = env('REDIS_DB_BRANDSITE_BACKEND', default='9')
REDIS_DB_REDIRECTION = env('REDIS_DB_REDIRECTION', default='2')

# Define Redis cache locations
DEFAULT_CACHE_LOCATION = f'redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB_DEFAULT}'
API_CACHE_LOCATION = f'redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB_API}'
API_THROTTLE_CACHE_LOCATION = f'redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB_API_THROTTLE}'
POST_API_CACHE_LOCATION = f'redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB_POST_API}'
BRANDSITE_BACKED_CACHE_LOCATION = f'redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB_BRANDSITE_BACKEND}'
REDIRECTION_CACHE_LOCATION = f'redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB_REDIRECTION}'

# Cache settings
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': DEFAULT_CACHE_LOCATION,
    },
    'api': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': API_CACHE_LOCATION,
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient'
        },
        'KEY_PREFIX': 'hdfclife'
    },
    'api_v1': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': API_CACHE_LOCATION,
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient'
        },
        'KEY_PREFIX': 'hdfclife'
    },
    'api_throttle': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': API_THROTTLE_CACHE_LOCATION,
    },
    'brandsite_backend': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': BRANDSITE_BACKED_CACHE_LOCATION,
        'TIMEOUT': None,
    },
    'post_api': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': POST_API_CACHE_LOCATION,
        'TIMEOUT': 60 * 60 * 1,  # Timeout of 1 Hr
    },
    'redirection': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': REDIRECTION_CACHE_LOCATION,
        'TIMEOUT': None,  # Never expire redirection keys
    },
}

# Cache configuration settings
ENABLE_CACHE = True
MAX_CACHE_EXPIRE_TIME = 3600
SINGLE_DAY_CACHE_TIMEOUT = 60 * 60 * 24  # 1 day
SEVEN_DAYS_CACHE_TIMEOUT = 60 * 60 * 24 * 7  # 7 days
HALF_HOUR_CACHE_TIMEOUT = 60 * 60 * 0.5
ONE_HOUR_CACHE_TIMEOUT = 60 * 60 * 1
VIEWCOUNT_CACHE_TIMEOUT = 60 * 60 * 24  # 1 day
MANUAL_RECENT_SEARCH_TERMS_TIMEOUT = 60 * 60 * 24 * 30  # One Month
MANUAL_TRENDING_SEARCH_TERMS_TIMEOUT = 60 * 60 * 24 * 7  # One Week
