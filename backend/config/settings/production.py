from .base import *  # noqa

DEBUG = False
SECURE_SSL_REDIRECT = env.bool("SECURE_SSL_REDIRECT", default=False)
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
