"""
Production settings for config project.
"""

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