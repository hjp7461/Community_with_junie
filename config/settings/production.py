"""
Production settings for config project.
"""

import os
from .base import *

# SECURITY WARNING: keep the secret key used in production secret!
# In production, this should be set from environment variables
SECRET_KEY = 'production-secret-key-should-be-set-from-environment-variables'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# Set your production hosts here
ALLOWED_HOSTS = ['example.com']

# HTTPS settings
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# Static files (CSS, JavaScript, Images)
# In production, these should be configured based on your deployment environment
# For example, you might use a CDN or a separate static file server
STATIC_URL = os.environ.get('STATIC_URL', '/static/')
STATIC_ROOT = os.path.join(BASE_DIR, os.environ.get('STATIC_ROOT', 'staticfiles'))
STATICFILES_DIRS = [os.path.join(BASE_DIR, os.environ.get('STATICFILES_DIR', 'static'))]

# Media files
# In production, these should be configured based on your deployment environment
# For example, you might use a cloud storage service like AWS S3
MEDIA_URL = os.environ.get('MEDIA_URL', '/media/')
MEDIA_ROOT = os.path.join(BASE_DIR, os.environ.get('MEDIA_ROOT', 'media'))
