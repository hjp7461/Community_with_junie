# Static and Media Files Configuration

## Overview
This document explains how static and media files are configured in the project based on the deployment environment.

## Configuration Structure
The project uses a modular settings structure with environment-specific settings files:
- `config/settings/base.py`: Common settings shared across all environments
- `config/settings/development.py`: Development-specific settings
- `config/settings/production.py`: Production-specific settings

## Static and Media Files Settings
Static and media files settings are now environment-specific and defined in the respective environment settings files.

### Development Environment
In the development environment, static and media files are stored locally:

```python
# Static files (CSS, JavaScript, Images)
STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'static']

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
```

### Production Environment
In the production environment, static and media files settings can be configured using environment variables:

```python
# Static files (CSS, JavaScript, Images)
STATIC_URL = os.environ.get('STATIC_URL', '/static/')
STATIC_ROOT = os.path.join(BASE_DIR, os.environ.get('STATIC_ROOT', 'staticfiles'))
STATICFILES_DIRS = [os.path.join(BASE_DIR, os.environ.get('STATICFILES_DIR', 'static'))]

# Media files
MEDIA_URL = os.environ.get('MEDIA_URL', '/media/')
MEDIA_ROOT = os.path.join(BASE_DIR, os.environ.get('MEDIA_ROOT', 'media'))
```

## Environment Variables
In the production environment, you can configure the following environment variables:

- `STATIC_URL`: The URL to use when referring to static files (default: '/static/')
- `STATIC_ROOT`: The directory where static files will be collected (default: 'staticfiles')
- `STATICFILES_DIR`: The directory where your static files are located (default: 'static')
- `MEDIA_URL`: The URL to use when referring to media files (default: '/media/')
- `MEDIA_ROOT`: The directory where media files will be stored (default: 'media')

## Deployment Considerations
When deploying to production, consider the following:

1. Set the appropriate environment variables for your deployment environment.
2. For static files, you might want to use a CDN or a separate static file server.
3. For media files, you might want to use a cloud storage service like AWS S3.
4. Make sure to run `python manage.py collectstatic` to collect all static files into the `STATIC_ROOT` directory.
5. Configure your web server (e.g., Nginx) to serve static and media files from the appropriate directories.

## Example: Using AWS S3 for Media Files
If you want to use AWS S3 for media files in production, you would:

1. Install the required packages:
   ```
   pip install django-storages boto3
   ```

2. Add 'storages' to INSTALLED_APPS in your production settings.

3. Configure AWS S3 settings in your production settings:
   ```python
   # AWS S3 settings
   AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
   AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
   AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME')
   AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'
   AWS_S3_OBJECT_PARAMETERS = {
       'CacheControl': 'max-age=86400',
   }
   
   # Media files
   DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
   MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/media/'
   ```

4. Set the required environment variables in your production environment.